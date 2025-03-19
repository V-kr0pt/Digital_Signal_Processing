#!/bin/bash

> ssim_128_results
for file in $(ls *_128.decod.pgm | sort -V); do
    image_name=$(echo "$file" | grep -oP '.*(?=_128.decod.pgm)')
    echo "$image_name - $file" #showing the progress
    echo "image=$image_name" >> ssim_128_results
    ./ssim.out "$image_name".pgm "$file" >> ssim_128_results
    echo "" >> ssim_128_results
done