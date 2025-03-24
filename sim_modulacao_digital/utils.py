import numpy as np

def db_to_linear(db):
    return 10 ** (db / 10)

def create_carrier_signal(data_length, carrier_power, carrier_freq, sampling_rate, bit_rate):
    """
    Gera um sinal senoidal com uma dada potência e frequência.

    Args:
        data_length (int): Comprimento dos dados.
        carrier_power (float): Potência da portadora (dB).
        carrier_freq (float): Frequência da portadora (Hz).
        bit_rate (float): Taxa de bits (bps).

    Returns:
        np.array: Sinal senoidal.
    """
    carrier_power = db_to_linear(carrier_power)  # Potência da portadora em escala linear
    A = np.sqrt(2 * carrier_power)  # Amplitude da portadora
    
    duration = 1 / bit_rate
    total_duration = duration * data_length
    number_of_points = int(sampling_rate * total_duration)
    t = np.linspace(0, total_duration, number_of_points, endpoint=False)

    return A * np.sin(2 * np.pi * carrier_freq * t)