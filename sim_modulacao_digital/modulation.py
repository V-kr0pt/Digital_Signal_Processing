import numpy as np
from utils import bits_to_int, dbm_to_linear

#  Função para codificação PSK
def psk_modulate(symbols, modulation_order):
    phases = 2 * np.pi * symbols / modulation_order
    return np.exp(1j * phases)  

def psk_modulation(data, modulation_order, samples_per_symbol, carrier_power=1, fc=1e3, fs=1e4):
    """
    Modula os dados binários usando PSK com uma portadora senoidal.

    Args:
        data (array): Dados binários (0s e 1s).
        modulation_order (int): Ordem da modulação PSK (ex: 2 para BPSK, 4 para QPSK, etc.).
        samples_per_symbol (int): Número de amostras por símbolo.
        carrier_power (float): Potência da portadora.
        fc (float): Frequência da portadora (Hz).
        fs (float): Frequência de amostragem (Hz).
    Returns:
        np.array: Sinal modulado PSK
    """

    # data should be organized in groups of log2(modulation_order)
    symbol_length = int(np.log2(modulation_order)) # Número de bits por símbolo
    try:
        binary_symbols = np.reshape(data, (-1, symbol_length)) # Reshape the data to groups of log2(modulation_order)
    except:
        # Se não for possível fazer o reshape, adiciona zeros à direita
        # Adiciona zeros à direita para completar o último símbolo
        padding_length = symbol_length - (len(data) % symbol_length)
        if padding_length < symbol_length:
            data = np.concatenate((data, np.zeros(padding_length, dtype=data.dtype)))
        binary_symbols = np.reshape(data, (-1, symbol_length)) # Reshape the data to groups of log2(modulation_order)

    # Convertendo os símbolos binários para inteiros
     # Converte os símbolos binários para inteiros
    symbols = bits_to_int(binary_symbols)  # Converte os símbolos binários para inteiros    
    symbols = symbols.flatten()  # Achata o array para uma dimensão
    symbols = symbols.astype(int)  # Converte para inteiro

    modulated = psk_modulate(symbols, modulation_order)

    # Valores I e Q por símbolo (antes de gerar o sinal)
    I = np.real(modulated) * np.sqrt(carrier_power)
    Q = np.imag(modulated) * np.sqrt(carrier_power)

    # Tempo total do sinal
    t = np.arange(0, len(symbols) * samples_per_symbol) / fs

    # Inicializa o sinal transmitido
    tx_signal = np.zeros(len(t))

    # Geração do sinal banda passante
    for i, symbol in enumerate(modulated):
        # Tempo para o símbolo atual
        t_symbol = t[i*samples_per_symbol : (i+1)*samples_per_symbol]

        # Modula com a portadora (cos para I, sin para Q)
        carrier = np.real(symbol) * np.cos(2 * np.pi * fc * t_symbol) - np.imag(symbol) * np.sin(2 * np.pi * fc * t_symbol)

        tx_signal[i*samples_per_symbol : (i+1)*samples_per_symbol] = np.sqrt(carrier_power)*carrier

    return tx_signal, modulated, np.repeat(symbols, samples_per_symbol), I, Q  # Retorna o sinal transmitido e o sinal modulado em banda base


def psk_demodulation(rx_signal, M,  samples_per_symbol, carrier_power, fc, fs):
    num_symbols = len(rx_signal) // samples_per_symbol
    num_symbols = int(num_symbols)
    samples_per_symbol = int(samples_per_symbol)
    # Tempo para um símbolo
    t_symbol = np.arange(samples_per_symbol) / fs
    
    # Portadoras vetorizadas
    cos_wave = np.cos(2 * np.pi * fc * t_symbol) 
    sin_wave = -np.sin(2 * np.pi * fc * t_symbol) 
    
    # Reshape para processar todos os símbolos de uma vez
    rx_matrix = rx_signal[:num_symbols * samples_per_symbol].reshape((num_symbols, samples_per_symbol))
    
    # Integra (soma) I e Q para todos símbolos em bloco
    I = 2/samples_per_symbol * np.dot(rx_matrix, cos_wave) 
    Q = 2/samples_per_symbol * np.dot(rx_matrix, sin_wave)
    
    # Calcula ângulo e decide símbolo mais próximo
    phases = np.arctan2(Q, I)
    phases[phases < 0] += 2 * np.pi  # Mantém entre 0 e 2pi
    
    symbols = np.round(phases * M / (2 * np.pi)) % M
    symbols = symbols.astype(int)
    # Converte de volta para bits
    bits_per_symbol = int(np.log2(M))
    bits = np.unpackbits(symbols.astype(np.uint8).reshape(-1, 1), axis=1)
    # Pega os últimos bits_per_symbol bits
    bits = bits[:, -bits_per_symbol:]  # dim(bits) = (num_simbols, ) each simbol has bits_per_symbol bits  
    return bits.flatten(), I, Q