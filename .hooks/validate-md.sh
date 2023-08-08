#!/bin/bash

tempfile=$(mktemp)
has_errors=false

function validate_readme
                         {
    file="$1"

    grep -q '^# [A-Za-z ]\+' "$file" || {
                                        echo "Error: Missing or malformed title in $file"
                                                                                           echo "true" > "$tempfile"
    }
    grep -q '^## Arguments' "$file" || {
                                       echo "Error: Missing Arguments section in $file"
                                                                                         echo "true" > "$tempfile"
    }
    grep -q '^## Pre-requisites' "$file" || {
                                            echo "Error: Missing Pre-requisites section in $file"
                                                                                                   echo "true" > "$tempfile"
    }
    grep -q '^## Examples' "$file" || {
                                      echo "Error: Missing Examples section in $file"
                                                                                       echo "true" > "$tempfile"
    }
    grep -q '^## Steps' "$file" || {
                                   echo "Error: Missing Steps section in $file"
                                                                                 echo "true" > "$tempfile"
    }
}

git ls-files | grep 'README.md$' | while read -r file; do
    if [ "$file" != "./README.md" ] && [ "$file" != "README.md" ]; then
        validate_readme "$file"
    fi
done

if [ -s "$tempfile" ]; then
    has_errors=true
fi

if [ "$has_errors" = false ]; then
    echo "All TTP docs (excluding root README.md) are in the expected format."
else
    echo "Validation failed for one or more TTP docs. Please review the errors above."
    exit 1
fi

# Clean up temporary file
rm -f "$tempfile"
