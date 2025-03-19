#!/bin/bash

> psnr_lena_results
for file in $(ls lena_*.decod.pgm | sort -V); do
    number=$(echo "$file" | grep -oP '(?<=lena_)\d+')
    echo "$number - $file" #showing the progress
    echo "N=$number" >> psnr_lena_results
    ./psnr.out lena.pgm "$file" >> psnr_lena_results
    echo "" >> psnr_lena_results
done