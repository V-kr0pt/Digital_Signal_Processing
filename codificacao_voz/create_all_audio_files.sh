# criando arquivos .dat usando PCM uniforme e .dat usando PCM mulaw
for bits in {7..1}; do
    ./Exp1/pcm_linear.out ./Exp1/seqtrei.dat "./output/saida_pcm_${bits}bits.dat" $bits
    ./Exp1/mulaw.out ./Exp1/seqtrei.dat "./output/saida_mu_${bits}bits.dat" $bits
done

