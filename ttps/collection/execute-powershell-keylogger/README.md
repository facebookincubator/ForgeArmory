# Input Capture

## Description
Captures keystrokes using PowerShell and Get-Keystrokes.ps1 script. Logs keyboard input to file, capturing passwords, usernames, and other sensitive data as users type.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **filepath**: Name of the local file where keystrokes will be logged, include path (default: `C:\Users\Public\key.log`)
- **keylogger_script_path**: Path to Get-Keystrokes.ps1 script (default: `./Get-Keystrokes.ps1`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP
2. The Get-Keystrokes.ps1 script must be present at the specified path

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//collection/powershell-keylogger/ttp.yaml \
  --filepath "C:\Temp\keylog.txt"
```

## Steps
1. **ensure_keylogger_script_exists**: Verifies that the Get-Keystrokes.ps1 script exists at the specified path before attempting to execute it. If the script is not found, the test exits with an error.
2. **capture_keystrokes**: Executes the Get-Keystrokes.ps1 script to begin capturing keystrokes and logging them to the specified file path.
