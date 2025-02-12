import os
import argparse
import time

from dft import dft
from fft_dit import fft_dit
from utils import read_input_file, write_output_file, plot_fft


def main(args):
    input_path = os.path.join(args.input)
    x = read_input_file(input_path)
    # o vetor de entrada de teste será um portão, 8 amostras
    #x = np.array([0, 1, 1, 1, 1, 0, 0, 0])
    # o vetor de entrada de teste será um portão, 64 amostras
    #x = np.array([0]+[1]*10+[0]*53)
    # o vetor de entrada de teste será uma sinc, 64 amostras
    #x = np.sinc(np.linspace(-4, 4, 64))

    # calculando a DFT
    if args.algo == 'fft':
        X = fft_dit(x)
    else:
        X = dft(x)
    # salvando o resultado no arquivo de saída (CORRIGIR)
    output_path = os.path.join(args.output)
    write_output_file(output_path, X)
    
    if args.save_plot:
        plot_fft(X)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input and output files.')
    parser.add_argument('--i', type=str, help='Input file name (a file of complex numbers representing the signal in time domain)')
    parser.add_argument('--o', type=str, default='a.out', help='Output file name (a file of complex numbers representing the signal in frequency domain)')
    parser.add_argument('--save_plot', action='store_true', default=False, help='Save plot of the signal in time and frequency domain into images folder')
    parser.add_argument('--algo', type=str, default='fft', help='Algorithm to use (dft or fft)')


    args = parser.parse_args()
    main(args)

