#!/bin/bash

for file in *_128.decod; do
    output="${file}.pgm"
    echo "Creating pgm for $file"
    ./dattopgm.out "$file" "$output"
done