import numpy as np
from utils import create_carrier_signal


NYQUIST_RATE = 4  # Taxa de Nyquist


def bpsk_modulation(data, carrier_power, carrier_freq, bit_rate):
    """
    Modula os dados binários usando BPSK com uma portadora senoidal.

    Args:
        data (array): Dados binários (0s e 1s).
        carrier_freq (float): Frequência da portadora (Hz).
        duration (float): Duração de cada bit (segundos).

    Returns:
        np.array: Sinal modulado BPSK.
    """
    # Fixar o sampling_rate como 4 vezes a frequência da portadora
    sampling_rate = NYQUIST_RATE * carrier_freq

    # Calcular o número total de amostras
    bit_period = 1 / bit_rate
    number_of_samples_per_bit = int(sampling_rate * bit_period)
    total_samples = len(data) * number_of_samples_per_bit
    
    # Gerar a portadora senoidal    
    carrier = create_carrier_signal(total_samples, carrier_power, carrier_freq, sampling_rate)

    # codificação bpsk
    data = bpsk_codification(data)

    # Repetir os bits para corresponder ao número de amostras por bit
    bit_repeated = np.repeat(data, number_of_samples_per_bit)

    return carrier * bit_repeated

def bpsk_demodulation(received_signal, carrier_power, carrier_freq, bit_rate):
    """
    Demodula um sinal BPSK. (demodulação coerente)

    Args:
        received_signal (array): Sinal recebido.
        carrier_freq (float): Frequência da portadora (Hz).
        sampling_rate (float): Taxa de amostragem (Hz).
        duration (float): Duração de cada bit (segundos).

    Returns:
        np.array: Dados binários demodulados.
    """
    bit_period = 1 / bit_rate # duração de cada bit

    sampling_rate = NYQUIST_RATE * carrier_freq
    number_of_samples_per_bit = int(sampling_rate * bit_period)
    total_samples = len(received_signal) # Número total de amostras
    
    # Comprimento dos dados
    #data_length = len(received_signal)/(sampling_rate*bit_period)
    #data_length = int(data_length) # Arredondar para o inteiro mais próximo

    # Gerar a portadora senoidal local
    carrier = create_carrier_signal(total_samples, carrier_power, carrier_freq, sampling_rate)

    # Multiplicar o sinal recebido pela portadora (correlação)
    correlated_signal = received_signal * carrier

    # Número de amostras por bit
    samples_per_bit = int(sampling_rate * bit_period)

    # Integrar o sinal para cada bit
    demodulated_bits = []
    for i in range(0, len(correlated_signal), samples_per_bit):
        # Somar os valores dentro do intervalo de um bit
        bit_energy = np.sum(correlated_signal[i:i + samples_per_bit])
        # Decidir o bit com base no sinal integrado
        demodulated_bits.append(1 if bit_energy > 0 else 0)

    return np.array(demodulated_bits)

#  Função para codificação BPSK
def bpsk_codification(data):
    data = data.astype(int) # Possibilita números negativos
    return 2 * data - 1  # Converte 0 e 1 para -1 e 1

#  Função para decodificação BPSK
def bpsk_decodification(received_signal):
    return (received_signal > 0).astype(int)