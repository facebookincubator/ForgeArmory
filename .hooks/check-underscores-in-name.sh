#!/bin/bash
set -e

git diff --cached --name-only --diff-filter=ACM | while IFS= read -r file; do
    echo "Checking file: $file"

    base_name=$(basename "$file")
    dir_name=$(dirname "$file")

    # Check if the base name of the file or directory has an underscore
    if [[ $base_name == *_* ]]; then
        # Conditions for YAML files or directories
        is_yaml_file=false
        if [[ "$file" == *.yml ]] || [[ "$file" == *.yaml ]]; then
            is_yaml_file=true
            echo "File $file is a YAML file."
        fi

        is_directory=false
        if [[ ! -f "$file" ]] && [[ -d "$file" ]]; then
            is_directory=true
            echo "File $file is a directory."
        fi

        if $is_yaml_file || $is_directory; then
            # Replace underscores with dashes using parameter expansion
            new_name=${base_name//_/-}

            # Check if the directory name is ".", which represents the root, and adjust accordingly
            new_path=$([[ "$dir_name" == "." ]] && echo "$new_name" || echo "$dir_name/$new_name")

            # Check if the file exists before trying to rename
            if [[ -e "$file" ]]; then
                git mv "$file" "$new_path"
                echo "Info: Renamed $file to $new_path using git mv."
            else
                echo "Info: $file doesn't exist, skipping..."
            fi
        fi
    else
        echo "$base_name does not have an underscore."
    fi
done

exit 0
