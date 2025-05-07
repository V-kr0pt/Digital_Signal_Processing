import streamlit as st
import numpy as np
import cv2
import matplotlib.pyplot as plt


from main import ImageTransmission


# Streamlit Interface
st.title("Visualização Interativa da Transmissão Digital de Imagens 📡🖼️")

# Upload da imagem
uploaded_file = st.file_uploader("Escolha uma imagem", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.subheader("Compreessão da Imagem")
    img = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (128, 128))
    
    # Lista de potências de 2 dentro do intervalo desejado
    potencias_de_2 = [2**i for i in range(1, 9)]  # De 2^1 (2) até 2^8 (256)
    algo_options = ['DCT', 'Vetorização']

    # Menu suspenso para selecionar o número de clusters
    algorithm = st.selectbox("Algoritmo de Compressão", algo_options, index=0) 
    num_clusters = st.selectbox("Número de Clusters (Vetores)", potencias_de_2, index=3)  # Valor padrão: 2^4 = 16


    st.subheader("Configurações da Transmissão")
    # Configurações do usuário
    modulation_method = st.selectbox("Escolha o método de modulação", ["ASK", "BPSK", "QPSK", "8PSK"], index=0)
    carrier_power = st.slider("Potência da Portadora (dBm)", min_value=-50, max_value=10, value=0)
    noise_power = st.slider("Potência do Ruído (dBm)", min_value=-50, max_value=10, value=10)
    list_of_symbol_rate_options = [100, 125, 160, 200, 250, 400, 500, 625, 1000,
                                    1250, 2000, 2500, 5000]
    symbol_rate = st.selectbox("Bound Rate (symbols/s)", list_of_symbol_rate_options)

    # Executar o algoritmo principal
    image_transmission = ImageTransmission(num_clusters, modulation_method, carrier_power, noise_power, symbol_rate)
    reconstructed_img, received_signal, modulated_signal, demodulated_data, transmited_symbols, execution_time= image_transmission.run(img)

    # Mostrar imagens lado a lado
    st.image([img, reconstructed_img], caption=["Imagem Original", "Imagem Reconstruída"], width=300)

    # Mostrar gráficos dos sinais
    st.markdown("### Sinais no Domínio do Tempo")
    hours_execution_time = execution_time // 3600
    minutes_execution_time = (execution_time % 3600) // 60
    seconds_execution_time = execution_time % 60
    
    # Apresenta o tempo de execução para o usuário
    st.write("O total de bits transmitido foi de ", len(modulated_signal), " bits")
    time_string = "O tempo necessário para enviar todos os bits foi de "
    if hours_execution_time > 0:
        time_string += f"{hours_execution_time:.0f} horas, "
    if minutes_execution_time > 0:
        time_string += f"{minutes_execution_time:.0f} minutos e "
    time_string += f"{seconds_execution_time:.0f} segundos"
    st.write(time_string)
    st.write("Total de tempo em segundos: ", execution_time, " segundos")
    
    
    symbol_time = 1 / symbol_rate  # Tempo de símbolo
    time_window = st.number_input("Tempo de Execução (s)", min_value=float(2*symbol_time),
                                   max_value=execution_time, value=float(2*symbol_time), step=float(symbol_time))
    
    fig, ax = plt.subplots(3, 1, figsize=(10, 6))

    t = np.linspace(0, execution_time, len(modulated_signal))
    num_points = int(len(t) * time_window / execution_time)

    modulation_method_dic = {
        'ASK': 2,
        'BPSK': 2,
        'QPSK': 4,
        '8PSK': 8
    }

    ax[0].plot(t[:num_points], transmited_symbols[:num_points], drawstyle='steps-post')
    ax[0].set_title(f"Dados Binários Transmitidos")
    ax[0].set_yticks(np.arange(0, modulation_method_dic[modulation_method], 1))
    ax[0].grid()
    ax[0].legend()
    
    ax[1].plot(t[:num_points], modulated_signal[:num_points], drawstyle='steps-post')
    ax[1].set_title(f"Sinal Modulado {modulation_method}")
    ax[1].grid()
    ax[1].legend()

    ax[2].plot(t[:num_points], received_signal[:num_points], drawstyle='steps-post')
    ax[2].set_title("Sinal Recebido")
    ax[2].grid()
    ax[2].legend()

    fig.tight_layout()

    st.pyplot(fig)