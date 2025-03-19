import os
import subprocess

def run_tests(input_dir, output_dir=None, time_filename='time.txt', algo='fft'):
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            print(f'Processing {filename} with {algo} algorithm')
            input_path = os.path.join(input_dir, filename)
            if output_dir is not None:
                output_path = os.path.join(output_dir, f'output_{filename}')
                cmd = [
                    'python', 'src/main.py', '--i', input_path, '--o', output_path, '--algo', algo, '--time', time_filename
                ]
            else:
                cmd = [
                    'python', 'src/main.py', '--i', input_path, '--algo', algo, '--time', time_filename, '--set_save_output_to_false'
                ]
            subprocess.run(cmd)
        
if __name__ == '__main__':
    input_dir = 'io_tests'
    #output_dir = 'io_tests/outputs'
    #os.makedirs(output_dir, exist_ok=True)
    
    # saving in the same file
    time_filename = 'test_time.csv'    
    run_tests(input_dir=input_dir, time_filename=time_filename, algo='fft')
    run_tests(input_dir=input_dir, time_filename=time_filename, algo='dft')