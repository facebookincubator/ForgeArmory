#!/bin/bash
set -ex

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed."
    exit 1
fi

COMMIT_MSG_FILE="$1"
NAME=$(git config user.name || echo "")
EMAIL=$(git config user.email || echo "")

# Ensure that the commit message file is provided and exists
if [[ -z "$COMMIT_MSG_FILE" || ! -f "$COMMIT_MSG_FILE" ]]; then
    echo "Error: Commit message file not provided or doesn't exist."
    exit 1
fi

# Check if NAME and EMAIL are set
if [[ -z "$NAME" || -z "$EMAIL" ]]; then
    echo "Error: Git user.name or user.email is not set."
    echo "Please configure them with:"
    echo "  git config --global user.name 'Your Name'"
    echo "  git config --global user.email 'youremail@example.com'"
    exit 1
fi

# Only append if the line doesn't already exist
if ! grep -q "Authored-by: $NAME <$EMAIL>" "$COMMIT_MSG_FILE"; then
    printf "\nAuthored-by: %s <%s>\n" "$NAME" "$EMAIL" >> "$COMMIT_MSG_FILE"
fi
