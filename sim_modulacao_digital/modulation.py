import numpy as np
from utils import create_carrier_signal


def bpsk_modulation(data, carrier_power, carrier_freq, duration):
    """
    Modula os dados binários usando BPSK com uma portadora senoidal.

    Args:
        data (array): Dados binários (0s e 1s).
        carrier_freq (float): Frequência da portadora (Hz).
        duration (float): Duração de cada bit (segundos).

    Returns:
        np.array: Sinal modulado BPSK.
    """

    # Fixar o sampling_rate como 10 vezes a frequência da portadora
    sampling_rate = 4 * carrier_freq
    
    carrier = create_carrier_signal(len(data), carrier_power, carrier_freq, sampling_rate, duration)
    
    # codificação bpsk
    data = bpsk_codification(data)

    # Repetir os bits para corresponder ao número de amostras por bit
    number_of_samples_per_bit = int(sampling_rate * duration)
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
    duration = 1 / bit_rate # duração de cada bit

    sampling_rate = 4 * carrier_freq

    # Comprimento dos dados
    data_length = len(received_signal)

    # Gerar a portadora senoidal local
    carrier = create_carrier_signal(data_length, carrier_power, carrier_freq, sampling_rate, bit_rate)

    # Multiplicar o sinal recebido pela portadora (correlação)
    correlated_signal = received_signal * carrier

    # Número de amostras por bit
    samples_per_bit = int(sampling_rate * duration)

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