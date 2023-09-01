#!/usr/bin/env bats

# Save the initial working directory
INITIAL_DIR="$(pwd)"

setup() {
	# Create a temporary directory
	TEMP_DIR=$(mktemp -d)

	# Change to the temporary directory
	cd "$TEMP_DIR" || exit

	# Initialize a git repo in the temp directory
	git init >/dev/null

	# Create test files and directory with underscores
	touch test_file_with_underscore.yaml
	mkdir test_directory_with_underscore

	# Stage the created files and directories
	git add .
}

teardown() {
	# Remove the temporary directory and all of its contents
	rm -rf "$TEMP_DIR"
	# Return to the original directory
	cd "$INITIAL_DIR" || exit
}

@test "Check if underscores in filenames are replaced with dashes" {
	# Run the pre-commit script using the initial directory to get the correct path
	"$INITIAL_DIR"/.hooks/check-underscores-in-name.sh

	# Check if files with dashes exist and are staged
	[ -f test-file-with-underscore.yaml ]
	git diff --cached --name-only | grep "test-file-with-underscore.yaml"
}

@test "Check if old filenames with underscores are not staged" {
	# Run the pre-commit script
	"$INITIAL_DIR"/.hooks/check-underscores-in-name.sh

	# Check if the old filenames/directories with underscores are not staged
	run git diff --cached --name-only
	[[ "$output" != *"test_file_with_underscore.yaml"* ]]

	run git diff --cached --name-only
	[[ "$output" != *"test_directory_with_underscore"* ]]
}
