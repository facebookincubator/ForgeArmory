# Creating W32Time similar named service using schtasks

## Description
Creates scheduled tasks with names similar to legitimate Windows services (e.g., "win32times" mimicking "W32Time") to evade detection. Used by "Operation Wocao" threat actor group. Configured to run with SYSTEM privileges and executes daily for persistent access.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **command**: Command to execute (default: `powershell.exe -c whoami`)
- **task_name**: Name of the scheduled task to create (default: `win32times`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/create-masqueraded-scheduled-task/ttp.yaml \
  --command "powershell.exe -c calc.exe" \
  --task_name "win32service"
```

## Steps
1. **create_masqueraded_scheduled_task**: Creates a scheduled task with a masqueraded name that mimics the W32Time service, configured to run as SYSTEM with daily scheduling, then queries the task to verify its creation.
