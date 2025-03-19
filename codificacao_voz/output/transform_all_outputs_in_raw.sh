for bits in {7..1}; do
    ../Exp1/dat2raw.out saida_mu_${bits}bits.dat audios/saida_mu_${bits}bits.raw
    ../Exp1/dat2raw.out saida_pcm_${bits}bits.dat audios/saida_pcm_${bits}bits.raw
done