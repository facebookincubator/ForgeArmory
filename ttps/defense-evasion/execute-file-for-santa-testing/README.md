# Execute File Blocked By SHA256 Hash In Santa

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP (Tactic, Technique, and Procedure) connects to a MacOS host that is running AppVote (Santa).
The script will then execute a precompiled binary and verify that Santa handles it appropriately (allows | blocks) by checking if the exit code is either `0` or `137`.

## Requirements

1. Host must be MacOS
2. Host must be running Santa

## Examples

You can run the TTP using the following example command (adjust arguments as
needed):

```bash
ttpforge run forgearmory//defense-evasion/execute-file-for-santa-testing/ttp.yaml --arg expected_exit_code=0
```

## Steps

1. **check_parameters**: Verify the argument `expected_exit_code` is either 0 or 137.
2. **verify_hash**: Verify the hash of the precompiled binary is what we expect.
3. **run_binary**: Run the precompiled binary, verify the exit code matches the expected code from parameters. By default, expects a `137` exit code indicating the application was killed by Santa.
