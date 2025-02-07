import numpy as np
from utils import permute_by_bit_reversal


def fft_dit(x):
    """
    Implementação da FFT com decimação no tempo (DIT-FFT, radix-2)
    """
    x = np.asarray(x, dtype=complex) # garantindo que x é um array de números complexos
    N = x.shape[0] # número de elementos

    if np.log2(N) % 1 > 0: # se o N não for uma potência de 2, o resto da divisão inteira de log2(N) por 1 será maior que 0.
        raise ValueError("O tamanho da entrada deve ser uma potência de 2")
    
    x = permute_by_bit_reversal(x, N)  # Reorganização em ordem reversa dos bit

    ... # Implementação da FFT