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

    reconstructed_img, modulated_signal, received_signal, demodulated_data= main(img, num_clusters, snr_db)

    # Mostrar imagens lado a lado
    st.image([img, reconstructed_img], caption=["Imagem Original", "Imagem Reconstruída"], width=300)

    # Mostrar gráficos dos sinais
    st.subheader("Sinais no Domínio do Tempo")
    fig, ax = plt.subplots(3, 1, figsize=(10, 6))

    ax[0].plot(modulated_signal[:100], label="Sinal Modulado (BPSK)")
    ax[0].legend()

    ax[1].plot(received_signal[:100], label="Sinal Recebido com Ruído", color='r')
    ax[1].legend()

    ax[2].plot(demodulated_data[:100], label="Sinal Demodulado", color='g')
    ax[2].legend()

    st.pyplot(fig)