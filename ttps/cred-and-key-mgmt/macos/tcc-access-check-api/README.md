# TCC Folder Access Checker Via API Calls

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP leverages MDQuery API calls to stealthily check for TCC folder
permissions.

## Pre-requisites

1. The code must be executed on a macOS system.
1. The user must have the necessary permissions to access the TCC folder and
   compile Swift code.
1. macOS Developer tools must be installed as the TTP requires Swift. To install
   developer tools:

   ```bash
   xcode-select --install
   ```

## Examples

You can run the TTP using a command execution framework, like so:

```bash
ttpforge run ttps/cred-and-key-mgmt/tcc_access_check_api/tcc_access_check_api.yaml \
    --arg detect=true
```

## Steps

1. **check**: This step compiles the Swift code using `swiftc` and executes
   the compiled binary to check TCC folder permissions for the current user.
   The result includes information about which folders have been accessed.

## Accompanying Code

The Swift code used in this TTP checks for Full Disk Access (FDA) and TCC
folder access permissions, and prints the results. It verifies access to user's
Desktop, Documents, and Downloads folders, and indicates if any access is
missing.

## MITRE ATT&CK Mapping

- **Tactics**:
  - T0009 Collection
- **Techniques**:
  - T1119 Automated Collection
