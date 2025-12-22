# WMI Invoke-CimMethod Scheduled Task

## Description
Creates scheduled tasks using WMI and Invoke-CimMethod PowerShell cmdlet. Leverages WMI's RegisterByXml method to create tasks from XML definitions. Can be executed remotely, blends with legitimate administrative activity, and bypasses security tools monitoring Task Scheduler API calls.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **xml_path**: Path to XML file for scheduled task definition (default: `./T1053_005_WMI.xml`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP
2. An XML file containing the scheduled task definition must exist at the specified path

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//persistence/create-scheduled-task-invoke-cimmethod/ttp.yaml \
  --xml_path "C:\Tasks\malicious-task.xml"
```

## Steps
1. **ensure_xml_file_exists**: Verifies that the XML file containing the scheduled task definition exists at the specified path before attempting task creation. If the file is not found, the test exits with an error.
2. **create_scheduled_task_via_wmi**: Reads the XML task definition from the file and uses Invoke-CimMethod to call the RegisterByXml method of the PS_ScheduledTask WMI class, creating a scheduled task that executes after user login.
