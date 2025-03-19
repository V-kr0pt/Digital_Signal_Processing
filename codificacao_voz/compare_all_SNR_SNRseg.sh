# criando um .txt e salvando os valores de SNR e SNRseg para cada arquivo .dat
for bits in {7..1}; do
    echo "SNR PCM ${bits}bits: " >> snr.txt
    ./Exp1/snr.out ./Exp1/seqtrei.dat "output/saida_pcm_${bits}bits.dat" >> snr.txt
    echo "" >> snr.txt
done

echo "======================" >> snr.txt

# fazendo o mesmo para PCM mulaw
for bits in {7..1}; do
    echo "SNR mu-law ${bits}bits: " >> snr.txt
    ./Exp1/snr.out ./Exp1/seqtrei.dat "output/saida_mu_${bits}bits.dat" >> snr.txt
    echo "" >> snr.txt
done
