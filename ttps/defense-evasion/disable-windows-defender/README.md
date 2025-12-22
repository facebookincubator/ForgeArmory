# Disable Windows Defender

## Description
Simulates methods to disable Windows Defender using registry tampering, PowerShell cmdlets, or service manipulation. Upon execution, Windows Defender protections will be significantly impaired or completely disabled.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **method**: The method to disable Windows Defender (choices: `registry`, `powershell`, `service`) (default: `registry`)
- **backup_location**: Path where first registry backup will be saved (for registry method) (default: `C:\Users\Public\backup.reg`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/disable-windows-defender/ttp.yaml \
  --method "powershell"
```

## Steps
1. **backup_registry_policies** (registry method only): Exports the entire HKLM\Software registry hive to a backup file.
2. **tamper_defender_registry_reg** (registry method): Modifies 16+ registry keys to disable all major Windows Defender protection features including AntiSpyware, AntiVirus, Behavior Monitoring, Intrusion Prevention, Real-Time Monitoring, Script Scanning, Enhanced Notifications, Cloud Protection, Potentially Unwanted Application detection, Tamper Protection, and Sample Submission.
3. **tamper_defender_atp** (powershell method): Uses Set-MpPreference cmdlets to disable Real-Time Monitoring, Behavior Monitoring, Script Scanning, and Block At First Seen features.
4. **tamper_defender_cmd** (service method): Stops the WinDefend service, configures it to disabled startup type, and queries the service status.
