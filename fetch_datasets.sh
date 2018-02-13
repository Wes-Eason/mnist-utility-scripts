#!/bin/bash
# This script downloads the MNIST handwriting datasets

# Check out this site for more info about the dataset
host="http://yann.lecun.com/exdb/mnist"

declare -a files
files[0]="train-images-idx3-ubyte.gz"
files[1]="train-labels-idx1-ubyte.gz"
files[2]="t10k-images-idx3-ubyte.gz"
files[3]="t10k-labels-idx1-ubyte.gz"

download_dir="mnist_data"

mkdir -p "$download_dir" || (echo "Failed to create folder (do you have permission?)" && exit 1)

echo "Fetching files from $host... (This should only take a few seconds)"

for file in ${files[*]}; do
    curl -s "$host/$file" | gunzip > "$download_dir/$(echo "$file" | sed 's/.gz$//g')" &
done

wait
