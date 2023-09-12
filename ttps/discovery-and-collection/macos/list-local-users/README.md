# macOS List Local User Accounts

![Community TTP - sw8y](https://img.shields.io/badge/Community_TTP-green)

Leverage Directory Service Command Line (DSCL) utility to gather local
user accounts.

## Pre-requisites

Ensure that `dscl` is installed on the target system and that you have the
necessary permissions to run it.

## Examples

Utilize `dscl` to view all local user accounts on the system. This TTP does
not produce artifacts, so it is not necessary to run the clean up afterward:

```bash
ttpforge run forgearmory//discovery-and-collection/macos/list-local-users/list-local-users.yaml
```

## Steps

1. **Run dscl**: Execute `dscl` to view all local user accounts on the system.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0007 Discovery
- **Techniques**:
  - T1087 Account Discovery
- **Sub-techniques**:
  - T1087.001 Local Account
