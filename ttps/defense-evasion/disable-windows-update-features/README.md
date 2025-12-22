# Disable Windows Update Features

## Description
Disables Windows Update features (auto-update and connection to Windows Update servers) through registry modifications. Prevents systems from receiving security patches, leaving them vulnerable to known exploits. Observed in Redline Stealer malware campaigns.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **backup_location_1**: Path where registry backup 1 will be saved (default: `C:\Users\Public\backup1.reg`)
- **backup_location_2**: Path where registry backup 2 will be saved (default: `C:\Users\Public\backup2.reg`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/disable-windows-update-features/ttp.yaml \
  --backup_location_1 "C:\Temp\backup1.reg" \
  --backup_location_2 "C:\Temp\backup2.reg"
```

## Steps
1. **disable_auto_update**: Modifies the NoAutoUpdate registry value in HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU, setting it to 1 to disable automatic Windows updates.
2. **disable_windows_update_connection**: Modifies the DoNotConnectToWindowsUpdateInternetLocations registry value in HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate, setting it to 1 to prevent the system from connecting to Windows Update servers.
