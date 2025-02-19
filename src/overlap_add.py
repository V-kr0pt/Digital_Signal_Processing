import numpy as np
from fft_dit import fft_dit, ifft_dit
from utils import read_input_file, write_output_file

def overlap_add_convolution(x, h, L):
    """ Implementa a convolução usando o método Overlap-Add com FFT DIT """
    N = 2**int(np.ceil(np.log2(len(h) + L - 1)))  # Garante que seja potência de 2
    H = fft_dit(np.pad(h, (0, N - len(h))))  # FFT do filtro h[n]

    y = np.zeros(len(x) + len(h) - 1)  # Inicializa a saída
    num_blocks = int(np.ceil(len(x) / L))  # Número de blocos

    for i in range(num_blocks):
        x_segment = x[i * L:(i + 1) * L]  # Pega um bloco do sinal de entrada
        x_padded = np.pad(x_segment, (0, N - len(x_segment)))  # Zero-padding
        X = fft_dit(x_padded)  # FFT do bloco

        Y_segment = ifft_dit(X * H).real  # Multiplicação e IFFT
        Y_segment = Y_segment[:len(h) + L - 1]  # ✅ Ajuste do tamanho

        y[i * L:i * L + len(Y_segment)] += Y_segment  # ✅ Evita erro de broadcasting


    return y

# Nomes dos arquivos
h_filename = "h.txt"  # Arquivo do filtro h[n]
x_filename = "x.txt"  # Arquivo do sinal x[n]
output_filename = "saida_convolucao_overlap_add.txt"

# Leitura dos sinais
h = read_input_file(h_filename, real_complex_format=False)
x = read_input_file(x_filename, real_complex_format=False)

# Define o tamanho do bloco L (por padrão, metade do tamanho da FFT ideal)
L = len(x) // 2

# Cálculo da convolução via Overlap-Add
y = overlap_add_convolution(x, h, L)

# Salva o resultado
write_output_file(output_filename, y, real_complex_format=False)

print(f"Convolução calculada e salva em '{output_filename}'")