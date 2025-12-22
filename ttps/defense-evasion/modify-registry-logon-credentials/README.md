# Modify registry to store logon credentials

## Description
Modifies Windows registry to force plaintext password storage in LSASS memory by setting WDigest UseLogonCredential to 1. Enables credential dumping tools like Mimikatz to extract cleartext passwords. Observed in numerous APT campaigns for lateral movement and privilege escalation.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **backup_location**: Path where registry backup will be saved (default: `C:\Users\Public\backup.reg`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/modify-registry-logon-credentials/ttp.yaml \
  --backup_location "C:\Temp\wdigest_backup.reg"
```

## Steps
1. **backup_registry**: Exports the current WDigest security provider registry settings from HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest to a backup file for restoration during cleanup.
2. **enable_wdigest_plaintext**: Adds or modifies the UseLogonCredential registry value in the WDigest security provider key, setting it to 1 (DWORD) to enable plaintext password caching in memory.
