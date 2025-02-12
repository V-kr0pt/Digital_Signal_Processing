import os
import argparse
import numpy as np
from fft_dit import fft_dit
from utils import read_input_file, write_output_file
from matplotlib import pyplot as plt

def main(args):
    input_path = os.path.join(args.input)
    x = read_input_file(input_path)
    # o vetor de entrada de teste será um portão, 8 amostras
    #x = np.array([0, 1, 1, 1, 1, 0, 0, 0])
    # o vetor de entrada de teste será um portão, 64 amostras
    #x = np.array([0]+[1]*10+[0]*53)
    # o vetor de entrada de teste será uma sinc, 64 amostras
    #x = np.sinc(np.linspace(-4, 4, 64))

    # calculando a FFT usando DIT
    X = fft_dit(x)

    # calculando DFT
    # ...

    # salvando o resultado no arquivo de saída
    output_path = os.path.join(args.output)
    write_output_file(output_path, X)

    if args.save_plot:
        X = np.fft.fftshift(X) #se quiser visualizar o espectro de frequência centralizado
        # plotando o sinal no tempo e o espectro de magnitude
        subplot = plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.stem(x)
        plt.title("Sinal no tempo")
        plt.subplot(2, 1, 2)
        plt.stem(np.abs(X))
        plt.title("Espectro de magnitude")

        # salvando a figura em images
        fig_path = os.path.join("images",args.input+".png")
        plt.savefig(fig_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input and output files.')
    parser.add_argument('--input', type=str, help='Input file name')
    parser.add_argument('--output', type=str, default='a.out', help='Output file name')
    parser.add_argument('--save_plot', action='store_true', default=False, )
    
    args = parser.parse_args()
    main(args)

