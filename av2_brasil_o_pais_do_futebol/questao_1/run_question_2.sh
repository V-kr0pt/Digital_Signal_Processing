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
    "dct"
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
# K = 4 bits 
K=2
N=256
./lbg.out "$K" "$N" 0.01 "seqtrei.dat" "seqtrei.dat" "dic_seqtrei.dic"

echo "Executando quantizador vetorial"
./codif_asc.out "$K" "$N" "dic_seqtrei.dic" "meutimefav.dat" "meutimefav_qv.cod"
./decodif_asc.out "$K" "$N" "dic_seqtrei.dic" "meutimefav_qv.cod" "output/meutimefav_qv.dat"

echo "Executando DCT com quantização"
./dct_qv_voz.out "meutimefav.dat" "output/meutimefav_dct.dat" 160 80 

> "output/SNR_SNRseg.txt"
# Executando cálculo da SNR
echo "Calculando SNR e SNRseg"
for tech in "${ALL_TECHNICS_LIST[@]}"; do
    input_file="output/meutimefav_$tech.dat"
    echo "$tech" >> "output/SNR_SNRseg.txt"
    ./snr.out "meutimefav.dat" "$input_file" >> "output/SNR_SNRseg.txt"
    echo "" >> "output/SNR_SNRseg.txt"
done

# transformando todos os arquivos .dat em output para .raw
for tech in "${ALL_TECHNICS_LIST[@]}"; do
    input_file="output/meutimefav_$tech.dat"
    output_file="output/meutimefav_$tech.raw"
    echo "Transformando $input_file para $output_file"
    ./dat2raw_8bits.out "$input_file" "$output_file"
done
