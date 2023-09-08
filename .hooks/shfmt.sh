#!/bin/bash
set -ex

# Loop through all arguments
for file in "$@"; do
    # Check if the file's path starts with 'templates/'
    if [[ $file != templates/* ]]; then
        shfmt -i 4 -bn -ci -sr -kp -fn -w "$file"
    else
        echo "Skipping formatting for $file"
    fi
done
