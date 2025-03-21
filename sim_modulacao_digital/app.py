import streamlit as st
import numpy as np
import cv2
import matplotlib.pyplot as plt


from main import main


# Streamlit Interface
st.title("Visualização Interativa da Transmissão Digital de Imagens 📡🖼️")

# Upload da imagem
uploaded_file = st.file_uploader("Escolha uma imagem", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (128, 128))
    
    # Configurações do usuário
    num_clusters = st.slider("Nível de Compressão (Número de Clusters)", min_value=4, max_value=128, value=16, step=2)
    snr_db = st.slider("SNR (dB)", min_value=-5, max_value=30, value=10)
    bit_rate = st.slider("Bit Rate", min_value=1, max_value=32, value=4)

    # Executar o algoritmo principal
    reconstructed_img, received_signal, modulated_signal, demodulated_data, execution_time= main(img, num_clusters, snr_db, bit_rate)

    # Mostrar imagens lado a lado
    st.image([img, reconstructed_img], caption=["Imagem Original", "Imagem Reconstruída"], width=300)

    # Mostrar gráficos dos sinais
    st.subheader("Sinais no Domínio do Tempo")
    time_window = st.slider("Tempo de Execução (s)", min_value=1., max_value=execution_time, value=1., step=1.)
    fig, ax = plt.subplots(2, 1, figsize=(10, 6))

    t = np.linspace(0, execution_time, len(modulated_signal))
    num_points = int(len(t) * time_window / execution_time)

    ax[0].plot(t[:num_points], modulated_signal[:num_points], drawstyle='steps-post', label="Sinal Modulado (BPSK)")
    ax[0].legend()

    ax[1].plot(t[:num_points], received_signal[:num_points], drawstyle='steps-post', label="Sinal Recebido com Ruído", color='r')
    ax[1].legend()

    st.pyplot(fig)