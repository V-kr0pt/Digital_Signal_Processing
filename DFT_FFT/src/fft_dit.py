import numpy as np
from utils import permute_by_bit_reversal


def fft_dit(x):
    """
    Implementação da FFT com decimação no tempo (DIT-FFT, radix-2)
    """
    x = np.asarray(x, dtype=complex) # garantindo que x é um array de números complexos
    N = x.shape[0] # número de elementos

    if np.log2(N) % 1 > 0: # se o N não for uma potência de 2, o resto da divisão inteira de log2(N) por 1 será maior que 0.
        # adiciona zeros para completar a potência de 2 (zero padding)
        zeros = np.zeros(2**int(np.log2(N)+1) - N, dtype=complex)
        x = np.concatenate((x, zeros))
    
    x = permute_by_bit_reversal(x, N)  # Reorganização em ordem reversa dos bit


    # pseudo-código encontrado em https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm 
    # com o nome de "iterative-fft" traduzido:
    for s in range(1, int(np.log2(N)) + 1): # para cada estágio s
        m = 2**s # número de pontos no subgrupo (2, 4, 8, ...)
        Wm = np.exp(-2j * np.pi / m) # fator de twiddle
        for k in range(0, N, m): # para cada subgrupo
            W = 1
            for j in range(m//2):
                t = W * x[k + j + m//2]
                u = x[k + j]
                x[k + j] = u + t
                x[k + j + m//2] = u - t
                W = W * Wm
    return x

def ifft_dit(X):
    """ Implementação da IFFT utilizando a FFT com DIT. """
    N = len(X)
    X_conj = np.conjugate(X)  # Conjugado para inverter
    x = fft_dit(X_conj)  # Aplica a FFT
    return np.conjugate(x) / N  # Conjugado de volta e divide por N