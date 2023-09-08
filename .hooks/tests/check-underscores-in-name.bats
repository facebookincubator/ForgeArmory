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
	git commit -m "Initial dummy commit"

	# Modify one of the files to introduce a change
	echo "dummy content" >>test_file_with_underscore.yaml

	# Stage the changes
	git add test_file_with_underscore.yaml
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

	# Debug: List all the files after running the script
	ls -al

	# Check if files with dashes exist
	[ -f test-file-with-underscore.yaml ]

	# Check if files with dashes are staged
	run git diff --cached --name-only
	[[ "$output" == *"test-file-with-underscore.yaml"* ]]
}

@test "Check if old filenames with underscores are not staged" {
	# Run the pre-commit script using the initial directory to get the correct path
	"$INITIAL_DIR"/.hooks/check-underscores-in-name.sh

	# Check the status of files
	run git status --porcelain
	trimmed_output=$(echo "$output" | tr -d ' ') # Remove whitespaces
	echo "Trimmed Git Status Output: $trimmed_output"

	# Ensure the old file is marked for deletion and the new file is added
	[[ $trimmed_output =~ Dtest_file_with_underscore.yaml ]]
	[[ $trimmed_output =~ Atest-file-with-underscore.yaml ]]

}
