import numpy as np
from fft_dit import fft_dit
from matplotlib import pyplot as plt

# o vetor de entrada de teste será um portão, 8 amostras
x = np.array([0, 1, 1, 1, 1, 0, 0, 0])
# o vetor de entrada de teste será um portão, 64 amostras
#x = np.array([0]+[1]*10+[0]*53)
# o vetor de entrada de teste será uma sinc, 64 amostras
#x = np.sinc(np.linspace(-4, 4, 64))

# calculando a FFT
X = fft_dit(x)
X = np.fft.fftshift(X) #se quiser visualizar o espectro de frequência centralizado

# plotando o sinal no tempo e o espectro de magnitude
subplot = plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.stem(x)
plt.title("Sinal no tempo")
plt.subplot(2, 1, 2)
plt.stem(np.abs(X))
plt.title("Espectro de magnitude")

# salvando a figura em images
plt.savefig("images/test1.png")