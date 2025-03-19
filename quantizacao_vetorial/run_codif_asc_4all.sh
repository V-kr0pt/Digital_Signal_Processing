#!/bin/bash

for file in *.dat; do
    # Skip the treino.dat file
    if [[ "$file" == "treino.dat" ]]; then
        continue
    fi
    output="${file%.dat}_128.cod"
    echo "Codifying $file"
    ./codif_asc.out 16 128 dic_all_128.dic "$file" "$output"
done