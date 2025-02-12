import os
import numpy as np
from matplotlib import pyplot as plt

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

def read_input_file(filename):
    """ Lê o arquivo de entrada e retorna um array numpy de números complexos. """
    data = []
    with open(filename, 'r') as f:
        for line in f:
            real, imag = map(float, line.split())
            data.append(complex(real, imag))
    return np.array(data)

def write_output_file(filename, X):
    """ Escreve os valores da DFT em um arquivo de saída. """
    with open(filename, 'w') as f:
        for value in X:
            f.write(f"{value.real:.6f} {value.imag:.6f}\n")

def plot_fft(filename:str, x:np.darray, X:np.darray):
    """
    Função que plota o sinal no tempo e na frequência e salva em "images"

    Parâmetros:
        filename: str - nome do arquivo de saída
        x: np.array - vetor no domínio do tempo
        X: np.array - vetor no domínio da frequência        
    
    Retorno:
        None    
    """
    X = np.fft.fftshift(X) #para visualizar o espectro de frequência centralizado
    # plotando o sinal no tempo e o espectro de magnitude
    subplot = plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.stem(x)
    plt.title("Sinal no tempo")
    plt.subplot(2, 1, 2)
    plt.stem(np.abs(X))
    plt.title("Espectro de magnitude")
    # salvando a figura em images
    fig_path = os.path.join("images",{filename}+".png")
    plt.savefig(fig_path)