#!/bin/bash

> ssim_lena_results
for file in $(ls lena_*.decod.pgm | sort -V); do
    number=$(echo "$file" | grep -oP '(?<=lena_)\d+')
    echo "$number - $file" #showing the progress
    echo "N=$number" >> ssim_lena_results
    ./ssim.out lena.pgm "$file" >> ssim_lena_results
    echo "" >> ssim_lena_results
done