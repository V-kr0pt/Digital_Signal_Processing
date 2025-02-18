import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('test_time.csv')
df = df.sort_values(by='N')
df_fft = df[df['Algo'] == 'fft']
df_dft = df[df['Algo'] == 'dft']

# plotting in the same graph
plt.plot(df_fft['N'], df_fft['Time'], label='FFT')
plt.plot(df_dft['N'], df_dft['Time'], label='DFT')
plt.xlabel('N')
plt.ylabel('Time (s)')
plt.legend()
plt.grid()
plt.title('Tempo de execução da DFT e FFT-DIT')
plt.savefig('images/execution_time.png')


# plotting in different graphs
fig, axs = plt.subplots(2, figsize=(10, 10))
fig.suptitle('Tempo de execução da DFT e FFT-DIT')
axs[0].plot(df_fft['N'], df_fft['Time'], label='FFT')
axs[0].set_title('FFT')
axs[0].set_xlabel('N')
axs[0].set_ylabel('Time (s)')
axs[0].grid()

axs[1].plot(df_dft['N'], df_dft['Time'], label='DFT')
axs[1].set_title('DFT')
axs[1].set_xlabel('N')
axs[1].set_ylabel('Time (s)')
axs[1].grid()

plt.savefig('images/execution_time_separated_graphs.png')