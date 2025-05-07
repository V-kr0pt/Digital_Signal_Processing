
import numpy as np

from compression import compress_image, reconstruct_image
from modulation import Modulation
from utils import dbm_to_linear

def add_noise(signal, noise_power):
    np.random.seed(42)
    noise = np.random.normal(0, noise_power, signal.shape)
    return signal + noise


class ImageTransmission:
    def __init__(self, num_clusters, modulation_method, carrier_power, noise_power, symbol_rate):
        # Compressão da imagem
        self.img = None
        self.num_clusters = num_clusters
        # check se o num_clursters é uma potência de dois
        if not np.log2(num_clusters).is_integer():
            raise ValueError("O número de clusters deve ser uma potência de 2")

        # Potência da portadora e do ruído
        self.snr_db = dbm_to_linear(noise_power)
        self.carrier_power = dbm_to_linear(carrier_power)

        # Parâmetros de modulação
        self.modulation = Modulation(modulation_method, symbol_rate, self.carrier_power, fc=1e4, fs=1e5)
        self.fc = self.modulation.fc
        self.fs = self.modulation.fs
        self.symbol_rate = symbol_rate
        self.M = self.modulation.modulation_order
    
        # incializando 
        self.reconstructed_img = None
        self.received_signal = None
        self.modulated_signal = None
        self.demodulated_data = None
        self.execution_time = None
        
        
    def run(self, img):
        self.img = img
        # Compressão
        labels, centroids, dct_shape = compress_image(self.img, self.num_clusters)

        # Converter índices de clusters para binário
        compressed_data = labels.reshape(-1)  # Flatten the quantized DCT coefficients

        # Transformando os índices em binário
        num_bits_per_vector = int(np.ceil(np.log2(self.num_clusters)))  # Número de bits necessários para criar um vetor com os num_clusters possíveis
        compressed_data_bin = np.unpackbits(compressed_data.astype(np.uint8).reshape(-1, 1), axis=1)

        # The unpack return 8 bits, and we're using the MSB (Most Significant Bits) first so we need to take the last num_bits
        compressed_data_bin = compressed_data_bin[:, -num_bits_per_vector:]  # dim(compressed_data_bin) = (num_simbols, ) each vector has num_bits_per_symbol bits
        self.compressed_data_bin = compressed_data_bin.flatten()
        
        # Modulação
        self.samples_per_symbol = int(self.fs / self.symbol_rate)
        self.modulated_signal, self.modulated_base_band, self.transmited_symbols, self.I_send, self.Q_send =\
              self.modulation.modulate(self.compressed_data_bin)

        # Transmissão com Ruído
        self.received_signal = add_noise(self.modulated_signal, self.snr_db)

        # Calcular o tempo de execução
        self.bit_rate = self.symbol_rate * self.M   # bits/s
        total_data_num_bits = self.compressed_data_bin.size 
        self.execution_time = total_data_num_bits/self.bit_rate  

        # Demodulação
        demodulated_data_bin, self.I_recv, self.Q_recv = self.modulation.demodulate(self.received_signal)
        # garanto que o tamanho é o sem padding adicionado durante a transmissão e recrio os vetores do dicionário
        demodulated_data_bin = demodulated_data_bin[:total_data_num_bits].reshape(-1, num_bits_per_vector).astype(np.uint8) 

        # Reconverter binário para índices de clusters
        # Adicionar zeros à esquerda para completar 8 bits
        demodulated_data_bin = np.hstack([np.zeros((demodulated_data_bin.shape[0], 8 - num_bits_per_vector),dtype=np.uint8),
                                          demodulated_data_bin], dtype=np.uint8)

        # Converter de binário para decimal
        self.demodulated_data = np.packbits(demodulated_data_bin, axis=1).flatten()
        self.demodulated_data = self.demodulated_data[:demodulated_data_bin.size]  # Ajustar tamanho

        # Garantir que os índices estejam no intervalo válido
        #demodulated_data = np.clip(demodulated_data, 0, num_clusters - 1)

        # Reconstrução da Imagem
        self.reconstructed_img = reconstruct_image(self.demodulated_data, centroids, dct_shape)
        self.reconstructed_img = np.clip(self.reconstructed_img, 0, 255) / 255.0
        self.img = self.img / 255.0  # Normalizar imagem original também

        return self.reconstructed_img, self.received_signal, self.modulated_signal, self.demodulated_data, self.transmited_symbols, self.execution_time



if __name__ == '__main__':
    import cv2
    import matplotlib.pyplot as plt

    img = cv2.imread('Lab.HAF_4968.jpg', cv2.IMREAD_GRAYSCALE) 
    img = cv2.resize(img, (128, 128))

    symbol_rate = 200
    modulation_method='8PSK'
    image_transmission = ImageTransmission(num_clusters=16, modulation_method=modulation_method, carrier_power=1, noise_power=-4, symbol_rate=symbol_rate)
    reconstructed_img, received_signal, modulated_signal, demodulated_data, transmited_symbols, execution_time = image_transmission.run(img)

    fig, ax = plt.subplots(3, 1, figsize=(10, 6))

    time_window = 2* symbol_rate
    t = np.linspace(0, execution_time, len(modulated_signal))
    num_points = int(len(t) * time_window / execution_time)

    ax[0].plot(t[:num_points], transmited_symbols[:num_points], drawstyle='steps-post', label="Dados Binários Transmitidos")
    ax[0].grid()
    ax[0].legend()
    
    ax[1].plot(t[:num_points], modulated_signal[:num_points], drawstyle='steps-post', label=f"Sinal Modulado {modulation_method}")
    ax[1].grid()
    ax[1].legend()

    ax[2].plot(t[:num_points], received_signal[:num_points], drawstyle='steps-post', label="Sinal Recebido com Ruído", color='r')
    ax[2].grid()
    ax[2].legend()

    plt.show()

    # Sinais no domínio do tempo
    t = np.linspace(0, 0.2, len(modulated_signal))
    fig, ax = plt.subplots(2, 1, figsize=(10, 6))
    ax[0].plot(t, modulated_signal, label="Sinal Modulado (BPSK)")
    ax[0].legend()

    ax[1].plot(t, received_signal, label="Sinal Recebido com Ruído", color='r')
    ax[1].legend()

    #ax[2].plot(t, demodulated_data, label="Sinal Demodulado", color='g')
    #ax[2].legend()

    plt.show()

    

    
