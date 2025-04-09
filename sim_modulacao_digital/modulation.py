#  Função para modulação BPSK
def bpsk_modulation(data):
    data = data.astype(int) # Possibilita números negativos
    return 2 * data - 1  # Converte 0 e 1 para -1 e 1

#  Função para demodulação BPSK
def bpsk_demodulation(received_signal):
    return (received_signal > 0).astype(int)