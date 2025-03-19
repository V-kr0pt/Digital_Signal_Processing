#!/bin/bash

for file in *.c; do
    output="${file%.c}.out"
    gcc -lm "$file" -o "$output"
done