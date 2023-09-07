#!/bin/bash
set -ex

# Change to the repository root
cd "$(git rev-parse --show-toplevel)"

# Determine the location of the mage binary
mage_bin=$(go env GOPATH)/bin/mage

# Check if mage is installed
if [[ -x "${mage_bin}" ]]; then
    echo "mage is installed"
else
    echo -e "mage is not installed\n"
    echo -e "Please install mage by running the following command:\n"
    echo -e "go install github.com/magefile/mage@latest\n"
    exit 1
fi

# Get the list of staged files ending with .yaml
staged_files=$(git diff --cached --name-only --diff-filter=AM | grep '\.yaml$')

# Variable to track whether validation failed
validation_failed=false

# Iterate over each staged file and validate it
for file in $staged_files; do
    "${mage_bin}" validateallyamlfiles docs/ttpforge-spec.yaml "$file"

    # Capture the exit code of the last validation
    exit_code=$?

    # If the exit code is not zero, set the flag to true
    if [ $exit_code -ne 0 ]; then
        validation_failed=true
    fi
done

# If any validation failed, exit with an error code
if [ "$validation_failed" = true ]; then
    echo "Validation failed for one or more YAML files."
    exit 1
fi
