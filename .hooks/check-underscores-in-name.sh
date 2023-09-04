#!/bin/bash
set -e

for file in $(git diff --cached --name-only --diff-filter=ACM); do
    echo "Checking file: $file"

    base_name=$(basename "$file")
    dir_name=$(dirname "$file")

    # Check if the base name of the file or directory has an underscore
    if [[ $base_name == *_* ]]; then

        if [[ "$file" == *.yml ]] || [[ "$file" == *.yaml ]] || {
                                                                  [[ ! -f "$file" ]] && [[ -d "$file" ]]
        }; then

            # Replace underscores with dashes using parameter expansion
            new_name=${base_name//_/-}
            # Check if the directory name is ".", which represents the root, and adjust accordingly
            new_path=$([[ "$dir_name" == "." ]] && echo "$new_name" || echo "$dir_name/$new_name")

            # Rename the file or directory and stage the change in Git
            git mv "$file" "$new_path"
            git reset HEAD "$file"

            echo "Info: Renamed $file to $new_path"
        fi
    else
        echo "$base_name does not have an underscore."
    fi
done

exit 0
