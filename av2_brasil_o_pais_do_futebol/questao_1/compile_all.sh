#!/bin/bash

for file in *.c; do
    output="${file%.c}.out"
    gcc "$file" -o "$output" -lm 
done