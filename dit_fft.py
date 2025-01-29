import numpy as np

def permute_by_bit_reversal(x:np.array, N:int) -> np.array:
    '''
    Função que reorganiza os elementos de um array x de tamanho N em ordem reversa dos bits.
    
    Parâmetros:
        x: np.array - array de entrada
        N: int - tamanho do array
    Retorno:
        np.array - array x reorganizado
    '''
    num_bits = int(np.log2(N))
    indices = np.arange(N, dtype=int)
    # reversão de bits está sendo feita através de uma compreensão de lista
    # para cada índice i, convertemos para binário com quantidade de bits: num_bits , 
    # invertemos a string [::-1] e convertemos de volta para inteiro
    reversed_indices = [int(f'{i:0{num_bits}b}'[::-1], 2) for i in indices]
    return x[reversed_indices]



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