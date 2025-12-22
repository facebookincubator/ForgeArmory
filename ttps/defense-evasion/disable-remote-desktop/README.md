# Disable Windows Remote Desktop Protocol

## Description
Disables RDP through registry modifications (setting fDenyTSConnections to 1) to prevent remote access and hinder incident response. Adversaries use this after establishing backdoors to prevent security teams from accessing compromised systems.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **backup_location**: Path where registry backup will be saved (default: `C:\Users\Public\backup.reg`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/disable-remote-desktop/ttp.yaml \
  --backup_location "C:\Temp\rdp_backup.reg"
```

## Steps
1. **backup_registry**: Exports the current Terminal Server registry settings to a backup file.
2. **disable_rdp**: Modifies the fDenyTSConnections registry value to 1 in HKLM\System\CurrentControlSet\Control\Terminal Server, effectively disabling Remote Desktop Protocol connections.
