# esse script busca automatizar a criação dos gráficos 
# de audio no tempo utilizando gnuplot.

# Frequência de amostragem
sampling_rate = 8000.0

# Arquivos que desejo criar o gráfico
files = system("ls *.dat")
n = words(files)

do for [i=1:n] {
	# Retirando a extensão do nome
	file = word(files, i)
	name = file[1:strstrt(file, '.dat')-1] # para nome do arquivo .png
	audio_name = name[1:strstrt(name,'_')-1] # para título do gráfico
	quantization_method = name[strstrt(name,'_')+1:*] # para título do gráfico

	# Nome do arquvio do gráfico
	set output sprintf('%s.png', name)
	set terminal pngcairo size 1280,720 enhanced font 'Verdana,10'

	# Título 
	set title sprintf("Áudio: %s | Método: %s", audio_name, quantization_method)
	set xlabel "Tempo (s)"
	set ylabel "Amplitude"
	set grid

	# Plot
	plot file using ($0/sampling_rate):1 with lines title quantization_method, \
		'meutimefav.dat' using ($0/sampling_rate):1 with lines lw 2 lc rgb "red" title "Original"
	}

