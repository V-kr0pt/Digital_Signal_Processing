import numpy as np
import time
from utils import read_input_file, write_output_file

def dft(x):
    """ Calcula a Transformada Discreta de Fourier (DFT) manualmente. """
    N = len(x)
    X = np.zeros(N, dtype=complex)
    for k in range(N):
        for n in range(N):
            X[k] += x[n] * np.exp(-2j * np.pi * k * n / N)
    return X

# Uso do programa
input_filename = "entrada.txt"
output_filename = "saida_dft.txt"

# Leitura dos dados de entrada
x = read_input_file(input_filename)

# Medição do tempo de execução
start_time = time.time()
X = dft(x)
end_time = time.time()

# Escrita dos resultados no arquivo de saída
write_output_file(output_filename, X)

# Tempo de execução
execution_time = end_time - start_time
print(f"Tempo de execução da DFT: {execution_time:.6f} segundos")