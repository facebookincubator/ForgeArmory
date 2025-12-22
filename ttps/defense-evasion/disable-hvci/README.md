# Disable Hypervisor-Enforced Code Integrity (HVCI)

## Description
Disables Hypervisor-Enforced Code Integrity (HVCI) by modifying registry settings. HVCI uses hardware virtualization to prevent malicious code injection and unsigned driver loading. This technique was used in the Black Lotus UEFI bootkit campaign (CVE-2022-21894).

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **backup_location**: Path where registry backup will be saved (default: `C:\Users\Public\backup.reg`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/disable-hvci/ttp.yaml \
  --backup_location "C:\Temp\hvci_backup.reg"
```

## Steps
1. **backup_registry**: Exports the current DeviceGuard registry settings to a backup file.
2. **disable_hvci**: Modifies the registry to disable HVCI by setting the Enabled value to 0 in HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity.
