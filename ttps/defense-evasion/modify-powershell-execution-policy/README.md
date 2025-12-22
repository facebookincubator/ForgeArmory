# Change Powershell Execution Policy to Bypass

## Description
Modifies PowerShell execution policy to Bypass, completely disabling script execution restrictions. Allows any PowerShell script to execute without security warnings. Commonly used by malware to ensure PowerShell payloads execute without triggering security blocks.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **default_execution_policy**: Specify the default poweshell execution policy (default: `Default`)
- **backup_location**: Path where registry backup will be saved (default: `C:\Users\Public\backup.reg`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/modify-powershell-execution-policy/ttp.yaml \
  --default_execution_policy "Restricted" \
  --backup_location "C:\Temp\ps_policy_backup.reg"
```

## Steps
1. **backup_registry**: Exports the current PowerShell execution policy registry settings from HKLM\SOFTWARE\Microsoft\PowerShell\1\ShellIds\Microsoft.PowerShell to a backup file for restoration during cleanup.
2. **set_execution_policy_bypass**: Uses Set-ExecutionPolicy cmdlet to set the execution policy to Bypass for the LocalMachine scope, allowing all PowerShell scripts to run without restrictions.
