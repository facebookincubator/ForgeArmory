# Abuse GPO Write Access to Add Scheduled Task

## Description

Abuses write access to a Group Policy Object (GPO) to create a scheduled task.
Supports specifying an arbitrary user context to run the task as.

## Arguments

- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: Username for authentication (without domain prefix). No default.
- **password**: Password for authentication. No default.
- **gpo_id**: The GPO GUID to modify (e.g., 12345677-ABCD-9876-ABCD-123456789012). No default.
- **command**: Command to execute via scheduled task. Defaults to `whoami > C:\Windows\Temp\task.txt`.
- **taskname**: Name of the scheduled task to create. Defaults to `GPOAbuseTask`.
- **run_as**: User context to run the task as. Defaults to `NT AUTHORITY\System`.
- **description**: Description of the scheduled task. Defaults to `Scheduled task created via GPO abuse`.

## Requirements

- Platform: Linux or macOS

## Example(s)

```bash
ttpforge run forgearmory//ttps/privilege-escalation/add-gpo-scheduled-task/ttp.yaml \
  --arg username=admin \
  --arg password=P@ssw0rd \
  --arg gpo_id=12345677-ABCD-9876-ABCD-123456789012 \
  --arg command="whoami > C:\Windows\Temp\task.txt" \
  --arg taskname=GPOAbuseTask
```

## Steps

1. **setup_impacket**: Set up Python virtual environment with impacket and ldap3.
2. **add_scheduled_task**: Add a scheduled task to the target GPO with the specified command and user context.
3. **Cleanup (add_scheduled_task)**: Remove the scheduled task from the GPO by running the script with the `--cleanup` flag.
