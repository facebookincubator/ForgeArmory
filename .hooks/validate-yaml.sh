#!/bin/bash
# This script is a pre-commit hook that checks if the mage command is
# installed and if not, prompts the user to install it. If mage is
# installed, the script changes to the repository root and runs the
# `mage validateyaml` command for each staged YAML file. This command
# validates all committed YAML files against a predefined schema. If any
# validation fails, the commit is stopped and an error message is shown.

set -e

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

if [[ -z "$staged_files" ]]; then
    echo "No YAML files to validate."
    exit 0
fi

# Iterate over each staged file and validate it
for file in $staged_files; do
    # Run the mage validateyaml command for the staged YAML file
    "${mage_bin}" validateyaml docs/ttpforge-spec.yaml "$file"

    # Catch the exit code of the last command
    exit_status=$?

    # If the exit code is not zero (i.e., the command failed),
    # then stop the commit and show an error message
    if [ $exit_status -ne 0 ]; then
        echo "Failed to validate YAML file '$file' against the schema."
        exit 1
    fi
done
