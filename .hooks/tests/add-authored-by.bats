#!/usr/bin/env bats

# Save the initial working directory
INITIAL_DIR="$(pwd)"
# Save the original path
ORIGINAL_PATH="$PATH"

setup() {
	# Create a temporary directory
	TEMP_DIR=$(mktemp -d)

	# Change to the temporary directory
	cd "$TEMP_DIR" || exit

	# Initialize a git repo in the temp directory
	git init >/dev/null

	# Create a dummy commit message file
	COMMIT_MSG_FILE="dummy_commit_msg.txt"
	echo "Initial commit message" >"$COMMIT_MSG_FILE"

	# Set git user details
	git config user.name "Test User"
	git config user.email "test@example.com"
}

teardown() {
	# Remove the temporary directory and all of its contents
	rm -rf "$TEMP_DIR"
	# Return to the original directory
	cd "$INITIAL_DIR" || exit
}

@test "Check if Authored-by line is appended to commit message" {
	# Run the pre-commit script using the initial directory to get the correct path
	"$INITIAL_DIR"/.hooks/add-authored-by.sh "$COMMIT_MSG_FILE"

	# Check if the Authored-by line is appended
	run grep "Authored-by: Test User <test@example.com>" "$COMMIT_MSG_FILE"
	[ "$status" -eq 0 ]
}

@test "Error when git is not installed" {
	# Modify PATH to mimic git not being available
	export PATH="/tmp"

	run "$INITIAL_DIR"/.hooks/add-authored-by.sh "$COMMIT_MSG_FILE"
	[ "$status" -ne 0 ]
	[[ "$output" == *"Error: git is not installed."* ]]

	# Reset PATH
	export PATH="$ORIGINAL_PATH"
}

@test "Error when git user.name or user.email is not set" {
	# Use a custom git configuration directory without any configurations set
	export GIT_CONFIG_NOSYSTEM=true
	HOME=$(mktemp -d)
	export HOME

	# Explicitly unset user.name and user.email
	git config --unset user.name
	git config --unset user.email

	run git config --get user.name

	run git config --get user.email

	run "$INITIAL_DIR"/.hooks/add-authored-by.sh "$COMMIT_MSG_FILE"
	[ "$status" -ne 0 ]
	[[ $output == *Error:\ Git\ user\.name\ or\ user\.email\ is\ not\ set\.* ]]
}
