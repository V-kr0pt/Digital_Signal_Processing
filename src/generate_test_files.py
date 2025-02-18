import numpy as np
from utils import write_output_file 

def generate_test_files(num_points_list, output_dir):
    for i, num_points in enumerate(num_points_list):
        filename = f'teste{i+1}.txt'
        filepath = os.path.join(output_dir, filename)
        x = np.random.rand(num_points) + 1j * np.random.rand(num_points)
        write_output_file(filepath, x)

if __name__ == '__main__':
    import os
    output_dir = 'io_tests' 
    os.makedirs(output_dir, exist_ok=True)
    
    num_files = 12
    num_points_list = [np.pow(2,num) for num in range(3,num_files+3)] # a partir de 8 pontos

    generate_test_files(num_points_list, output_dir)