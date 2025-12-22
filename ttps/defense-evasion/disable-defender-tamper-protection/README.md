# Tamper Win Defender Protection

## Description
Modifies Windows Defender's Tamper Protection registry value. Tamper Protection prevents unauthorized changes to security settings, even by administrators. RedLine Stealer malware uses this technique to weaken Windows Defender's defensive capabilities. Requires SYSTEM-level privileges.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **backup_location**: Path where registry backup will be saved (default: `C:\Users\Public\backup.reg`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/disable-defender-tamper-protection/ttp.yaml \
  --backup_location "C:\Temp\defender_backup.reg"
```

## Steps
1. **backup_registry**: Exports the current Windows Defender Features registry key to a backup file.
2. **tamper_defender_protection**: Modifies the TamperProtection registry value in HKLM\SOFTWARE\Microsoft\Windows Defender\Features, setting it to 0 to attempt disabling Tamper Protection.
