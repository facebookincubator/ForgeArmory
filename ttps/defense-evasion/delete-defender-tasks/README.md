# Delete Windows Defender Scheduled Tasks

## Description
Deletes Windows Defender scheduled tasks (Scheduled Scan, Cleanup, Verification, Cache Maintenance), degrading Defender's effectiveness without completely disabling it. Observed in Gootloader malware campaigns. Tasks are backed up before deletion for restoration during cleanup.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **backup_path**: Path to store the backup of the scheduled tasks (default: `C:\Users\Public`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/delete-defender-tasks/ttp.yaml \
  --backup_path "C:\Temp\Backup"
```

## Steps
1. **backup_scheduled_tasks**: Exports the XML definitions of all four Windows Defender scheduled tasks (Scheduled Scan, Cleanup, Verification, and Cache Maintenance) to the specified backup directory.
2. **delete_scheduled_tasks**: Deletes the four Windows Defender scheduled tasks if their backup files exist, effectively disabling Windows Defender's automated scanning and maintenance capabilities.
