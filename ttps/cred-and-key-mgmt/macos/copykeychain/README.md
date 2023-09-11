# Copy Keychain

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP copies the user's login keychain database to the `/tmp` directory.

## Arguments

- **detect:** If set to true, the script will check the log file for entries
  indicating the copy operation and report if any suspicious activity is
  detected. Default value is `true`.

## Pre-requisites

1. The user must have the necessary permissions to access and copy the
   keychain database.
1. This TTP is specific to macOS, where the login keychain database resides.

## Examples

You can run the TTP using the following example:

```bash
ttpforge run forgearmory//cred-and-key-mgmt/macos/copykeychain/copykeychain.yaml
```

## Steps

1. **copykeychain**: This step utilizes the `cp` command to copy the user's
   login keychain database from `~/Library/Keychains/login.keychain-db` to
   `/tmp/keychain-copied`.
1. **log-keychain-copying**: Logs the copy operation of the login keychain
   database to the user's home directory. Contains a cleanup process that
   removes the copied keychain after 10 seconds.
1. **check-detection**: If the `detect` argument is set to true, this step
   checks the log file for entries indicating the copy operation and reports if
   any suspicious activity is detected.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0006 Credential Access
- **Techniques**:
  - T1555 Credentials from Password Stores
- **Sub-techniques**:
  - T1555.001 Credentials from Password Stores: Keychain
