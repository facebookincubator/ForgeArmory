#!/bin/bash
set -ex

# Run all bats tests in the tests directory
output=$(bats ".hooks/tests/"*.bats)
exit_code=$?

echo "${output}"
exit ${exit_code}
