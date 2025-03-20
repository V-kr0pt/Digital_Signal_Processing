
import numpy as np

from compression import compress_image, reconstruct_image
from modulation import bpsk_modulation, bpsk_demodulation

def add_noise(signal, snr_db):
    snr_linear = 10 ** (snr_db / 10)
    noise = np.random.normal(0, np.sqrt(1 / (2 * snr_linear)), signal.shape)
    return signal + noise


def main(img, num_clusters, snr_db):
   
    # Compressão
    labels, centroids, dct_shape = compress_image(img, num_clusters)

    # Converter índices de clusters para binário
    compressed_data = labels.reshape(-1)  # Flatten the quantized DCT coefficients
    
    # Transformando os índices em binário
    num_bits = int(np.ceil(np.log2(num_clusters)))  # Número de bits necessários
    compressed_data_bin = np.unpackbits(compressed_data.astype(np.uint8).reshape(-1, 1), axis=1)
    
    # The unpack return 8 bits, and we're using the MSB (Most Significant Bits) first so we need to take the last num_bits
    compressed_data_bin = compressed_data_bin[:, -num_bits:]   
    
    # Modulação
    modulated_signal = bpsk_modulation(compressed_data_bin.flatten())

    # Transmissão com Ruído
    received_signal = add_noise(modulated_signal, snr_db)

    # Demodulação
    demodulated_data_bin = bpsk_demodulation(received_signal).reshape(-1, num_bits).astype(np.uint8)

    # Reconverter binário para índices de clusters
    # Adicionar zeros à esquerda para completar 8 bits
    demodulated_data_bin = np.hstack([np.zeros((demodulated_data_bin.shape[0], 8 - num_bits),dtype=np.uint8),
                                      demodulated_data_bin], dtype=np.uint8)
    
    # Converter de binário para decimal
    demodulated_data = np.packbits(demodulated_data_bin, axis=1).flatten()
    demodulated_data = demodulated_data[:demodulated_data_bin.size]  # Ajustar tamanho

    # Garantir que os índices estejam no intervalo válido
    #demodulated_data = np.clip(demodulated_data, 0, num_clusters - 1)

    # Reconstrução da Imagem
    reconstructed_img = reconstruct_image(demodulated_data, centroids, dct_shape)
    reconstructed_img = np.clip(reconstructed_img, 0, 255) / 255.0
    img = img / 255.0  # Normalizar imagem original também

    return reconstructed_img, received_signal, modulated_signal, demodulated_data



if __name__ == '__main__':
    import cv2
    import matplotlib.pyplot as plt

    img = cv2.imread('Lab.HAF_4968.jpg', cv2.IMREAD_GRAYSCALE) 
    img = cv2.resize(img, (128, 128))

    reconstructed_img, received_signal, modulated_signal, demodulated_data = main(img, 8, 10)


    # Mostrar imagens lado a lado
    fig, ax = plt.subplots(1, 2, figsize=(10, 6))
    ax[0].imshow(img, cmap='gray')
    ax[0].set_title("Imagem Original")
    ax[0].axis('off')

    ax[1].imshow(reconstructed_img, cmap='gray')
    ax[1].set_title("Imagem Reconstruída")
    ax[1].axis('off')

    plt.show()

    # Sinais no domínio do tempo
    fig, ax = plt.subplots(3, 1, figsize=(10, 6))
    ax[0].plot(modulated_signal[:100], label="Sinal Modulado (BPSK)")
    ax[0].legend()

    ax[1].plot(received_signal[:100], label="Sinal Recebido com Ruído", color='r')
    ax[1].legend()

    ax[2].plot(demodulated_data[:100], label="Sinal Demodulado", color='g')
    ax[2].legend()

    plt.show()

    

    
