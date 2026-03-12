# Execute File Blocked By SHA256 Hash In MDE

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP (Tactic, Technique, and Procedure) connects to a host that is running Microsoft Endpoint Defender (MDE).
It will check for the existence of a file. If the file is not present, we assume that is because MDE has blocked it.
Otherwise, it will attempt to execute the file with a SHA256 hash that has been previously been blocked in MDE, and verifies that the exit code from that execution is an "Operation not permitted" (126).

## Requirements

1. Host must be running Microsoft Endpoint Defender
2. File hash must be blocked in MDE.

## Examples

You can run the TTP using the following example command (adjust arguments as
needed):

```bash
ttpforge run forgearmory//defense-evasion/create-and-execute-blocked-file/ttp.yaml \
```

## Steps

1. **verify_and_execute_file**:
     Checks if the file is present. If it is not, we consider this a successful result since that means it was quarantined by MDE.

     If it is present, grant execution permission on it.

     Print out the hash for debugging purposes

     Execute the file to ensure the appropriate exit code is returned.

This is all done in a single step so we can gracefully exit the script
if the file has been blocked and removed by MDE.
