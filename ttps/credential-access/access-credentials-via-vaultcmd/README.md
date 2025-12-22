# Access Saved Credentials via VaultCmd

## Description
Enumerates credentials stored in Windows Credential Manager using vaultcmd.exe. This native Windows utility can list usernames, passwords, and authentication information for websites, applications, and network resources.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//credential-access/access-credentials-via-vaultcmd/ttp.yaml
```

## Steps
1. **list_windows_credentials**: Executes vaultcmd.exe with the /listcreds parameter to enumerate credentials stored in the "Windows Credentials" vault.
