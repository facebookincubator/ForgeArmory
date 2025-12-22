# Abusing MyComputer Path for Persistence

## Description
Abuses Windows MyComputer registry paths (BackupPath, CleanupPath, DefragPath) to hijack system maintenance operations. Executes malicious payloads whenever users trigger maintenance activities. Provides persistence and defense evasion by appearing as legitimate system maintenance.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **method**: Method to use for persistence (choices: `backup`, `cleanup`, `defrag`) (default: `backup`)
- **executable_path**: Custom Executable to run (default: `C:\Windows\System32\cmd.exe`)
- **backup_location**: Path where registry backup will be saved (default: `C:\Users\Public\backup.reg`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//persistence/add-mycomputer-executable/ttp.yaml \
  --method "cleanup" \
  --executable_path "C:\Malware\payload.exe"
```

## Steps
1. **backup_registry**: Exports the current MyComputer registry settings to a backup file for restoration during cleanup.
2. **add_registry_entry**: Modifies the specified MyComputer registry path (BackupPath, CleanupPath, or DefragPath) to point to the custom executable specified in the executable_path argument, establishing persistence through system maintenance operation hijacking.
