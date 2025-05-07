
import numpy as np

from compression import compress_image, reconstruct_image
from modulation import psk_modulation, psk_demodulation
from utils import dbm_to_linear

def add_noise(signal, noise_power):
    np.random.seed(42)
    noise_power_linear = dbm_to_linear(noise_power) # convert from dBm to linear scale
    noise = np.random.normal(0, noise_power_linear, signal.shape)
    return signal + noise


class ImageTransmission:
    def __init__(self, num_clusters, modulation_method, carrier_power, noise_power, symbol_rate):
        self.img = None
        self.num_clusters = num_clusters
        self.snr_db = noise_power
        self.carrier_power = carrier_power
        self.symbol_rate = symbol_rate
        self.fc = 1e4  # Frequência da portadora (Hz)
        self.fs = 1e5  # Frequência de amostragem (Hz)
        #self.samples_per_symbol = 100
        self.M = 4 # ordem de modulação PSK
        self.reconstructed_img = None
        self.received_signal = None
        self.modulated_signal = None
        self.demodulated_data = None
        self.execution_time = None

        if modulation_method != 'ASK':
            if modulation_method == 'BPSK':
                self.M = 2
            elif modulation_method == 'QPSK':
                self.M = 4
            elif modulation_method == '8PSK':
                self.M = 8
            else:
                raise ValueError("Método de modulação inválido. Escolha entre 'ASK', 'BPSK', 'QPSK' ou '8PSK'.")
        else:
            ...


        # check se o num_clursters é uma potência de dois
        if not np.log2(num_clusters).is_integer():
            raise ValueError("O número de clusters deve ser uma potência de 2")

    def run(self, img):
        self.img = img
        # Compressão
        labels, centroids, dct_shape = compress_image(self.img, self.num_clusters)

        # Converter índices de clusters para binário
        compressed_data = labels.reshape(-1)  # Flatten the quantized DCT coefficients

        # Transformando os índices em binário
        num_bits_per_symbol = int(np.ceil(np.log2(self.num_clusters)))  # Número de bits necessários para criar um símbolo com os num_clusters possíveis
        compressed_data_bin = np.unpackbits(compressed_data.astype(np.uint8).reshape(-1, 1), axis=1)

        # The unpack return 8 bits, and we're using the MSB (Most Significant Bits) first so we need to take the last num_bits
        compressed_data_bin = compressed_data_bin[:, -num_bits_per_symbol:]  # dim(compressed_data_bin) = (num_simbols, ) each simbol has num_bits_per_symbol bits
        self.compressed_data_bin = compressed_data_bin.flatten()
        
        # Tempo necessário para enviar todos os bits
        self.bit_rate = self.symbol_rate * num_bits_per_symbol  # bits/s
        total_data_num_bits = self.compressed_data_bin.size 
        self.execution_time = total_data_num_bits/self.bit_rate  

        # Modulação
        self.samples_per_symbol = int(self.fs / self.symbol_rate)
        self.modulated_signal, self.modulated_base_band, self.transmited_symbols = psk_modulation(self.compressed_data_bin,
                                                                                              self.M, self.samples_per_symbol,
                                                                                                self.carrier_power, self.fc, self.fs)

        # Transmissão com Ruído
        self.received_signal = add_noise(self.modulated_signal, self.snr_db)

        # Demodulação
        demodulated_data_bin = psk_demodulation(self.received_signal, self.M, self.samples_per_symbol, self.carrier_power, self.fc, self.fs)
        # garanto que o tamanho é o sem padding adicionado durante a transmissão e recrio os vetores do dicionário
        demodulated_data_bin = demodulated_data_bin[:total_data_num_bits].reshape(-1, num_bits_per_symbol).astype(np.uint8) 

        # Reconverter binário para índices de clusters
        # Adicionar zeros à esquerda para completar 8 bits
        demodulated_data_bin = np.hstack([np.zeros((demodulated_data_bin.shape[0], 8 - num_bits_per_symbol),dtype=np.uint8),
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

    bit_rate = 100
    modulation_method='8PSK'
    image_transmission = ImageTransmission(num_clusters=16, modulation_method=modulation_method, carrier_power=1, noise_power=-4, symbol_rate=bit_rate)
    reconstructed_img, received_signal, modulated_signal, demodulated_data, transmited_symbols, execution_time = image_transmission.run(img)

    fig, ax = plt.subplots(3, 1, figsize=(10, 6))

    time_window = 2* bit_rate
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

    

    
