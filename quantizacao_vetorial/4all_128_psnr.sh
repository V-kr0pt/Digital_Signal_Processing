#!/bin/bash

> psnr_128_results
for file in $(ls *_128.decod.pgm | sort -V); do
    image_name=$(echo "$file" | grep -oP '.*(?=_128.decod.pgm)')
    echo "$image_name - $file" #showing the progress
    echo "image=$image_name" >> psnr_128_results
    ./psnr.out "$image_name".pgm "$file" >> psnr_128_results
    echo "" >> psnr_128_results
done