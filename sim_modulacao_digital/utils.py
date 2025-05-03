import numpy as np

def db_to_linear(db):
    return 10 ** (db / 10)

def create_carrier_signal(total_samples, carrier_power, carrier_freq, sampling_rate):
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
    t = np.arange(total_samples) / sampling_rate

    return A * np.sin(2 * np.pi * carrier_freq * t)