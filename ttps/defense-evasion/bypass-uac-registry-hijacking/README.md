# Bypass UAC via Registry Hijacking

## Description
Bypasses UAC using registry hijacking by exploiting auto-elevated Windows executables (eventvwr.exe, fodhelper.exe, ComputerDefaults.exe, sdclt.exe). Hijacks execution flow through registry modification to run arbitrary commands with elevated privileges without generating UAC prompts.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **executable_binary**: Binary to execute with UAC Bypass (default: `fodhelper`)
- **command_to_execute**: Command to execute for sdclt method (default: `cmd.exe /c notepad.exe`)
- **backup_file_path**: File path to backup UAC settings (default: `C:\Users\Public\backup.reg`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/bypass-uac-registry-hijacking/ttp.yaml \
  --executable_binary "computerdefaults" \
  --command_to_execute "cmd.exe /c calc.exe"
```

## Steps
1. **backup_uac_settings**: Exports the current UAC-related registry settings to a backup file.
2. **bypass_uac**: Creates a new registry key at HKCU:\Software\Classes\Folder\shell\open\command with the specified command, sets the DelegateExecute property, and starts the chosen auto-elevated executable to trigger the UAC bypass.
