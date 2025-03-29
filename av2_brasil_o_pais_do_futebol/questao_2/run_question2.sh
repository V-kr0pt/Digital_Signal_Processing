#!/bin/bash

# Define número de níveis e dicionários
N=(512 1024)
DICTIONARYS=("dic_all" "dic_lena")


# codifica para os diferentes Ns e dicionários
for dic in "${DICTIONARYS[@]}"; do
    for n in "${N[@]}"; do
        for file in *.dat; do
            # Skip the treino.dat file
            if [[ "$file" == "treino.dat" ]]; then
                continue
            fi
            output="${file%.dat}_${n}_${dic}.cod"
            echo "Codifying $file with N=$n and dictionary $dic"
            ./codif_asc.out 16 "$n" "${dic}_${n}.dic" "$file" "$output"
            echo "Codification of $file with N=$n done"
        done
    done
done


# decodifica para os diferentes Ns e dicionários
for dic in "${DICTIONARYS[@]}"; do
    for n in "${N[@]}"; do
        for file in *_${n}_${dic}.cod; do
            output="${file%.cod}.decod"
            echo "Decodifying $file"
            ./decodif_asc.out 16 "$n" "${dic}_${n}.dic" "$file" "$output"
            echo "Decodification of $file with N=$n done"
        done
    done
done


# converte os arquivos decodificados para PGM
for dic in "${DICTIONARYS[@]}"; do
    for n in "${N[@]}"; do
        for file in *_${n}_${dic}.decod; do
            output="${file}.pgm"
            echo "Creating pgm for $file"
            ./dattopgm.out "$file" "$output"
        done
    done
done


# Avalia PSNR e SSIM e joga em um arquivo .txt
> psnr_results
for dic in "${DICTIONARYS[@]}"; do
    for n in "${N[@]}"; do
        echo "Dic=$dic | N=$n" >> psnr_results
        for file in *_${n}_${dic}.decod.pgm; do
            original_file="${file%_${n}_${dic}.decod.pgm}.pgm"
            echo "$file" >> psnr_results
            ./psnr.out "$original_file" "$file" >> psnr_results
            echo "" >> psnr_results
        done
    done
done

> ssim_results
for dic in "${DICTIONARYS[@]}"; do
    for n in "${N[@]}"; do
        echo "Dic=$dic | N=$n" >> ssim_results
        for file in *_${n}_${dic}.decod.pgm; do
            original_file="${file%_${n}_${dic}.decod.pgm}.pgm"
            echo "$file" >> ssim_results
            ./ssim.out "$original_file" "$file" >> ssim_results
            echo "" >> ssim_results
        done
    done
done

# Move todos os arquivos gerados para a pasta output
mkdir -p output
for dic in "${DICTIONARYS[@]}"; do
    for n in "${N[@]}"; do
        for file in *_${n}_${dic}.decod.pgm; do
            mv "$file" output/
        done

        # Move todos os arquivos .cod de saída para a pasta de saída
        for file in *_${n}_${dic}.cod; do
            mv "$file" output/
        done
        
        # Move todos os arquivos .decod de saída para a pasta de saída
        for file in *_${n}_${dic}.decod; do
            mv "$file" output/
        done
    done
done

mv ssim_results output/
mv psnr_results output/