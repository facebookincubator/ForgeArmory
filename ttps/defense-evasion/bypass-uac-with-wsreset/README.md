# UAC Bypass with WSReset Registry Modification

## Description
Bypasses UAC on Windows 10 1803/1809 by exploiting WSReset.exe, a Windows Store troubleshooting tool that auto-elevates without UAC prompts. Hijacks execution flow through registry modification to run arbitrary commands with elevated privileges. Limited to specific Windows 10 versions.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **command_path**: Registry path (default: `HKCU:\Software\Classes\AppX82a6gwre4fdg3bt635tn5ctqjf8msdd2\Shell\open\command`)
- **command_to_run**: Command to run (default: `C:\Windows\System32\cmd.exe /c start cmd.exe`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/bypass-uac-with-wsreset/ttp.yaml \
  --command_to_run "C:\Windows\System32\calc.exe"
```

## Steps
1. **bypass_uac_wsreset**: Creates the hijack registry key, sets the DelegateExecute property, modifies the default command value to execute the specified payload, and launches WSReset.exe in a hidden window to trigger the UAC bypass.
