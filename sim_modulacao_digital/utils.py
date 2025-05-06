import numpy as np

def dbm_to_linear(dbm_power):
    return 1e-3*10 ** (dbm_power / 10)

def bits_to_int(arr):
    # Calcula pesos: 2^(posições invertidas)
    weights = 2 ** np.arange(arr.shape[1]-1, -1, -1)
    # Faz o produto e soma
    return arr @ weights


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
    carrier_power = dbm_to_linear(carrier_power)  # Potência da portadora em escala linear
    A = np.sqrt(2 * carrier_power)  # Amplitude da portadora
    t = np.arange(total_samples) / sampling_rate

    return A * np.sin(2 * np.pi * carrier_freq * t)