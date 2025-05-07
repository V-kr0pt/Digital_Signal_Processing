import numpy as np
from utils import bits_to_int, dbm_to_linear

class Modulation:
    def __init__(self, set_modulation, symbol_rate, carrier_power=1, fc=1e4, fs=1e5):
        self.set_modulation = set_modulation
        self.carrier_power = carrier_power
        self.fc = fc
        self.fs = fs
        self.samples_per_symbol = int(fs / symbol_rate)
        self.define_modulation_order()

    def define_modulation_order(self):
        if self.set_modulation == 'ASK':
            self.modulation_order = 2
        elif self.set_modulation == 'BPSK':
            self.modulation_order = 2
        elif self.set_modulation == 'QPSK':
            self.modulation_order = 4
        elif self.set_modulation == '8PSK':
            self.modulation_order = 8
        else:
            raise ValueError("Método de modulação inválido. Escolha entre 'ASK', 'BPSK', 'QPSK' ou '8PSK'.")

    def modulate(self, data):
        if self.set_modulation[-3:] == 'ASK':
            return self.ask_modulation(data, self.modulation_order, self.samples_per_symbol, self.carrier_power, self.fc, self.fs)
        elif self.set_modulation[-3:] == 'PSK':
            return self.psk_modulation(data, self.modulation_order, self.samples_per_symbol, self.carrier_power, self.fc, self.fs)
        else:
            raise NotImplementedError("Método de modulação não implementado.")

    def demodulate(self, rx_signal):
        if self.set_modulation[-3:] == 'ASK':
            return self.ask_demodulation(rx_signal, self.modulation_order, self.samples_per_symbol, self.carrier_power, self.fc, self.fs)
        elif self.set_modulation[-3:] == 'PSK':
            return self.psk_demodulation(rx_signal, self.modulation_order, self.samples_per_symbol, self.carrier_power, self.fc, self.fs)
        else:
            raise NotImplementedError("Método de demodulação não implementado.")
        
    def create_binary_symbols(self, data, modulation_order):
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
        
        return binary_symbols

    def ask_modulation(self, data, modulation_order, samples_per_symbol, carrier_power=1, fc=1e3, fs=1e4):
        """
        Modula os dados binários usando ASK com uma portadora senoidal.

        Args:
            data (array): Dados binários (0s e 1s).
            modulation_order (int): Ordem da modulação ASK.
            samples_per_symbol (int): Número de amostras por símbolo.
            carrier_power (float): Potência da portadora.
            fc (float): Frequência da portadora (Hz).
            fs (float): Frequência de amostragem (Hz).

        Returns:
            np.array: Sinal modulado ASK
        """


        # Criando os símbolos binários
        binary_symbols = self.create_binary_symbols(data, modulation_order)

        # Convertendo os símbolos binários para inteiros
        symbols = bits_to_int(binary_symbols)  # Converte os símbolos binários para inteiros    
        symbols = symbols.flatten()  # Achata o array para uma dimensão
        symbols = symbols.astype(int)  # Converte para inteiro

        I = symbols * np.sqrt(carrier_power)  # Valores I por símbolo
        Q = np.zeros_like(I)  # Valores Q por símbolo (zero para ASK)

        # Tempo total do sinal
        t = np.arange(0, len(symbols) * samples_per_symbol) / fs

        # Inicializa o sinal transmitido
        tx_signal = np.zeros(len(t))

        # Geração do sinal banda passante
        for i, symbol in enumerate(symbols):
            # Tempo para o símbolo atual
            t_symbol = t[i*samples_per_symbol : (i+1)*samples_per_symbol]

            # Modula com a portadora
            carrier = np.sqrt(carrier_power) * symbol * np.cos(2 * np.pi * fc * t_symbol)

            tx_signal[i*samples_per_symbol : (i+1)*samples_per_symbol] = carrier

        return tx_signal, symbols, np.repeat(symbols, samples_per_symbol), I, Q

    def ask_demodulation(self, rx_signal, modulation_order, samples_per_symbol, carrier_power, fc, fs):
        num_symbols = len(rx_signal) // samples_per_symbol
        num_symbols = int(num_symbols)
        samples_per_symbol = int(samples_per_symbol)
        # Tempo para um símbolo
        t_symbol = np.arange(samples_per_symbol) / fs

        # Portadoras vetorizadas
        cos_wave = np.cos(2 * np.pi * fc * t_symbol)

        # Reshape para processar todos os símbolos de uma vez
        rx_matrix = rx_signal[:num_symbols * samples_per_symbol].reshape((num_symbols, samples_per_symbol))

        # Integra (soma) I e Q para todos símbolos em bloco
        I = 2/samples_per_symbol * np.dot(rx_matrix, cos_wave)
        Q = np.zeros_like(I)

        # Calcula ângulo e decide símbolo mais próximo
        amplitudes = I/np.sqrt(carrier_power)
        #symbols = np.round(amplitudes).astype(int)
        #symbols = np.clip(symbols, 0, modulation_order - 1)

        # Definindo os símbolos válidos (0, 1, 2, ..., M-1)
        possible_symbols = np.arange(modulation_order)

        # Decisão usando distância mínima
        symbols = np.array([possible_symbols[np.argmin(np.abs(i - possible_symbols))] for i in amplitudes])


        # Converte de volta para bits
        bits_per_symbol = int(np.log2(modulation_order))
        bits = np.unpackbits(symbols.astype(np.uint8).reshape(-1, 1), axis=1)
        # Pega os últimos bits_per_symbol bits
        bits = bits[:, -bits_per_symbol:]  # dim(bits) = (num_simbols, ) each simbol has bits_per_symbol bits  
        return bits.flatten(), I, Q


    #  Função para codificação PSK
    def psk_modulate(self, symbols, modulation_order):
        phases = 2 * np.pi * symbols / modulation_order
        return np.exp(1j * phases)  

    def psk_modulation(self, data, modulation_order, samples_per_symbol, carrier_power=1, fc=1e3, fs=1e4):
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

        binary_symbols = self.create_binary_symbols(data, modulation_order)  # Cria os símbolos binários

        # Convertendo os símbolos binários para inteiros
        symbols = bits_to_int(binary_symbols)  # Converte os símbolos binários para inteiros    
        symbols = symbols.flatten()  # Achata o array para uma dimensão
        symbols = symbols.astype(int)  # Converte para inteiro

        modulated = self.psk_modulate(symbols, modulation_order)

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


    def psk_demodulation(self, rx_signal, M,  samples_per_symbol, carrier_power, fc, fs):
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


    def qam_modulation(self, data, modulation_order, samples_per_symbol, carrier_power=1, fc=1e3, fs=1e4):
        bits_per_symbol = int(np.log2(modulation_order))
        # Ajusta o tamanho para múltiplo do bits_per_symbol
        padding = (-len(data)) % bits_per_symbol
        if padding:
            data = np.concatenate((data, np.zeros(padding, dtype=int)))

        # Converte bits para inteiros
        symbols = np.packbits(data).astype(int)
        symbols = symbols[:len(data)//bits_per_symbol]

        # Gera constelação QAM normalizada
        M = int(np.sqrt(modulation_order))
        I = 2 * (symbols % M) - (M - 1)
        Q = 2 * (symbols // M) - (M - 1)
        qam_symbols = I + 1j * Q
        qam_symbols /= np.sqrt((2/3)*(modulation_order - 1))  # Normalização de potência média = 1

        # Geração do sinal banda passante
        t = np.arange(len(symbols) * samples_per_symbol) / fs
        tx_signal = np.zeros_like(t)

        for i, sym in enumerate(qam_symbols):
            t_sym = t[i*samples_per_symbol : (i+1)*samples_per_symbol]
            carrier = np.real(sym) * np.cos(2 * np.pi * fc * t_sym) - np.imag(sym) * np.sin(2 * np.pi * fc * t_sym)
            tx_signal[i*samples_per_symbol : (i+1)*samples_per_symbol] = np.sqrt(carrier_power) * carrier

        return tx_signal, qam_symbols, np.repeat(symbols, samples_per_symbol), I, Q


    def qam_demodulation(self, rx_signal, modulation_order, samples_per_symbol, carrier_power, fc, fs):
        num_symbols = len(rx_signal) // samples_per_symbol
        samples_per_symbol = int(samples_per_symbol)
        t_symbol = np.arange(samples_per_symbol) / fs

        cos_wave = np.cos(2 * np.pi * fc * t_symbol) * np.sqrt(carrier_power)
        sin_wave = -np.sin(2 * np.pi * fc * t_symbol) * np.sqrt(carrier_power)

        rx_matrix = rx_signal[:num_symbols * samples_per_symbol].reshape((num_symbols, samples_per_symbol))

        # Normalização correta da energia
        I = (2 / samples_per_symbol) * np.dot(rx_matrix, cos_wave)
        Q = (2 / samples_per_symbol) * np.dot(rx_matrix, sin_wave)

        # Normaliza a constelação para o grid original
        norm_factor = np.sqrt((2/3)*(modulation_order - 1))
        I /= norm_factor
        Q /= norm_factor

        M = int(np.sqrt(modulation_order))
        I_symbols = np.clip(np.round((I + (M - 1)) / 2), 0, M-1)
        Q_symbols = np.clip(np.round((Q + (M - 1)) / 2), 0, M-1)

        symbols = (Q_symbols * M + I_symbols).astype(int)

        bits_per_symbol = int(np.log2(modulation_order))
        bits = np.unpackbits(symbols.astype(np.uint8).reshape(-1, 1), axis=1)
        bits = bits[:, -bits_per_symbol:]
        return bits.flatten(), I, Q