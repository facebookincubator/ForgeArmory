# Windows Powershell Logging Disabled

## Description
Disables PowerShell logging (Module Logging, Script Block Logging, Transcription, Script Execution) through registry modifications. Prevents security teams from identifying malicious PowerShell usage and investigating attack chains.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **backup_location**: Path where registry backup will be saved (default: `C:\Users\Public\backup.reg`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/disable-powershell-logging/ttp.yaml \
  --backup_location "C:\Temp\ps_logging_backup.reg"
```

## Steps
1. **backup_registry**: Exports the current PowerShell logging registry settings to a backup file.
2. **disable_powershell_logging**: Modifies multiple registry keys to disable PowerShell Module Logging, Script Block Logging, Transcription, and Script Execution by setting their enable values to 0, then deletes the EnableScripts value.
