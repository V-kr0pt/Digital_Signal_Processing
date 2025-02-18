import argparse
import time

from dft import dft
from fft_dit import fft_dit
from utils import read_input_file, write_output_file, save_execution_time, plot_fft


def main(input, output, algo='fft', save_plot=False, time_filename=None, save_output=True):

    x = read_input_file(input)
  
    start_time = time.time()
    # calculando a DFT
    if algo == 'fft':
        X = fft_dit(x)
    else:
        X = dft(x)
    total_time = time.time() - start_time

    if time_filename:
        save_execution_time(time_filename, total_time, len(x), algo)
    
    # salvando o resultado no arquivo de saída
    if save_output:
        write_output_file(output, X)
    
    if save_plot:
        plot_fft(input, x, X)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input and output files.')
    parser.add_argument('--i', type=str, default='entrada.txt', help='Input file name (a file of complex numbers representing the signal in time domain)')
    parser.add_argument('--o', type=str, default='saida.txt', help='Output file name (a file of complex numbers representing the signal in frequency domain)')
    parser.add_argument('--save_plot', action='store_true', default=False, help='Save plot of the signal in time and frequency domain into images folder')
    parser.add_argument('--algo', type=str, default='fft', help='Algorithm to use (dft or fft)')
    parser.add_argument('--time', type=str, help='The name of the file to save the execution time')
    parser.add_argument('--set_save_output_to_false', action='store_false', default=True, help='Set to False to not save the output file')


    args = parser.parse_args()
    main(args.i, args.o, args.algo, args.save_plot, args.time, args.set_save_output_to_false)

