# Bypass UAC using SilentCleanup task

## Description
Bypasses UAC by exploiting the auto-elevated SilentCleanup scheduled task on Windows 8-10. Modifies the %windir% environment variable to inject malicious commands that execute with Administrator privileges when the task is triggered. Works even at highest UAC levels without user interaction.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **bat_file_path**: Path to the bat file (default: `./T1548.002.bat`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/bypass-uac-using-silentcleanup-task/ttp.yaml \
  --bat_file_path "C:\Scripts\bypass.bat"
```

## Steps
1. **ensure_bat_file_exists**: Verifies that the batch file exists at the specified path before attempting execution. If the bat file is not found, the test exits with an error.
2. **execute_silentcleanup_bypass**: Executes the batch file that performs the SilentCleanup UAC bypass by modifying the windir environment variable and forcefully running the SilentCleanup scheduled task to achieve elevated command execution.
