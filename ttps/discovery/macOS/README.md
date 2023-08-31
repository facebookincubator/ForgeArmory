# macOS List Local User Accounts

![Community TTP - sw8y](https://img.shields.io/badge/Community_TTP-green)

Leverage Directory Service Command Line (DSCL) utility to gather local user accounts.

## Pre-requisites

Ensure that dscl is installed on the target system and that you have the necessary
permissions to run it.

## Examples

Utilize dscl to view all local user accounts on the system. This TTP does not produce
artifacts, so it is not necessary to run the clean up afterward:

```bash
ttpforge run ttps/discovery/macOS/list_local_users/list_local_users.yaml
```

## Steps

1. **Run dscl**: Execute dscl to view all local user accounts on the system.
