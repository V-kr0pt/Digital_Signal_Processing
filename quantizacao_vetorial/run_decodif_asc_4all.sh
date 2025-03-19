#!/bin/bash

for file in *_128.cod; do
    output="${file%.cod}.decod"
    echo "Decodifying $file"
    ./decodif_asc.out 16 128 dic_all_128.dic "$file" "$output"
done