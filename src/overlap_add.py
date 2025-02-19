import numpy as np
from fft_dit import fft_dit, ifft_dit
from utils import read_input_file, write_output_file

def overlap_add_convolution(x, h, L):
    """ Implementa a convolução usando o método Overlap-Add com FFT DIT """
    n = len(h) + L - 1 # tamanho resultante de cada operação de convolução
    N = 2**int(np.ceil(np.log2(n)))  # Garantindo que seja potência de 2 

    y = np.zeros(len(x) + len(h) - 1)  # Inicializa a saída com tamanho resultante da operação de convolução do sinal de entrada com o filtro
    num_segments = int(np.ceil(len(x) / L))  # Número de segmentos

    H = fft_dit(np.pad(h, (0, N - len(h))))  # FFT do filtro h[n] padding para garantir o tamanho do segmento 
    for i in range(num_segments):
        x_seg = x[i * L:(i + 1) * L]  # Segmento do sinal de entrada de tamanho L
        x_pad = np.pad(x_seg, (0, N - len(x_seg)))  # Zero-padding para garantir o tamanho do segmento seja o tamanho resultante da operação de convolução

        # Domínio da frequência
        X = fft_dit(x_pad)  # FFT do bloco
        Y = X * H  # Multiplicação no domínio da frequência = convolução no domínio do tempo

        # retorno ao domínio do tempo
        y_seg = ifft_dit(Y).real  # IFFT
        y_seg = y_seg.real  # obtendo a parte real
        y_seg = y_seg[:n]  # retirando o zero-padding

        y[i * L:i * L + len(y_seg)] += y_seg  # Adiciona o resultado do segmento ao sinal de saída (overlap-add)


    return y

if __name__ == '__main__':
    # Nomes dos arquivos
    import os
    io_folder = 'overlap_add_io'
    h_filename = os.path.join(io_folder,"h.txt")  # Arquivo do filtro h[n]
    x_filename = os.path.join(io_folder,"x.txt")  # Arquivo do sinal x[n]
    output_filename = os.path.join(io_folder,"saida_convolucao_overlap_add.txt")

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