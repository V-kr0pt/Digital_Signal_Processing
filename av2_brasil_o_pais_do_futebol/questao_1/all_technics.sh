#!/bin/bash

TECHNICS_LIST=(
    "quantizador"
    "alaw"
    "mulaw"
)

ALL_TECHNICS_LIST=(
    "quantizador"
    "alaw"
    "mulaw"
    "qv"
#    "dct"
)

echo "Transformando o arquivo de raw para dat"
./raw2dat_8bits.out "meutimefav.raw" "meutimefav.dat"
echo "Add zeros to the end of the file"
# Adicionando zeros no final do arquivo
echo "0" >> "meutimefav.dat"

mkdir -p "output"

for tech in "${TECHNICS_LIST[@]}"; do
    file="${tech}.out"
    output_file="meutimefav_$tech.dat"
    echo "Executando $file"
    ./"$file" "meutimefav.dat" "output/$output_file" 4
done

echo "criando dicionário para quantizador vetorial"
# K = 4 bits -> L = 16 níveis 
./lbg.out 4 512 0.00001 "meutimefav.dat" "meutimefav.dat" "dic_meutimefav.dic"

echo "Executando quantizador vetorial"
./codif_asc.out 4 512 "dic_meutimefav.dic" "meutimefav.dat" "meutimefav_qv.cod"
./decodif_asc.out 4 512 "dic_meutimefav.dic" "meutimefav_qv.cod" "output/meutimefav_qv.dat"

echo "Executando DCT com quantização"
# Flávio disse que era 160 180
# 8bits/amostra -> eu desejo transformar para 4bits/amostra 
# num_de_amostra_original = 9974
# num_de_bits=4 -> num_de_amostras = 16 
# 9974/16 = 623,625 -> arredondando para 622
# -> comprimento de cada amostra= 622; 622*16 = 9952
# 9974 - 9952 = 22 -> maior multiplo de 16 mais próximo 36 = 2*16
# descarte de 2 amostras por cada 16 amostras

#./dct_voz.out "meutimefav.dat" "output/meutimefav_dct.dat" 160 180 

> "output/SNR_SNRseg.txt"
# Executando cálculo da SNR
echo "Calculando SNR e SNRseg"
for tech in "${ALL_TECHNICS_LIST[@]}"; do
    input_file="output/meutimefav_$tech.dat"
    echo "$tech" >> "output/SNR_SNRseg.txt"
    ./snr.out "meutimefav.dat" "$input_file" >> "output/SNR_SNRseg.txt"
    echo "" >> "output/SNR_SNRseg.txt"
done

