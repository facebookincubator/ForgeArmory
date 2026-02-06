##  Description:
This script creates a scheduled task in Windows using the Task Scheduler COM API. The task will execute a specified action (default is cmd.exe) under a specified principal (default is SYSTEM). The task will start after a specified trigger time (default is 1 minute) and repeat at a specified interval (default is 30 minutes).

## Dependencies:
- pywin32 library (install with `pip install pywin32`)
- ctypes library (built-in Python library)

## Usage:
```
python create_scheduled_task.py [options]
```

## Options:
- `--name`: Name of the task (default: "HighPriorityPyCOMTask")
- `--action`: Path of the action to execute (default: C:\Windows\System32\cmd.exe)
- `--trigger`: Minutes until the task starts (default: 1)
- `--repeat`: Repeat interval in minutes (default: 30)
- `--principal`: Principal under which to run the task (default: "SYSTEM")

## Example:
```
python create_scheduled_task.py --name MyTask --action C:\Path\To\MyScript.exe --trigger 5 --repeat 60 --principal ADMIN
```

## MITRE Attack Mapping:
- T1053: Scheduled Task/Job ( creation of a scheduled task to execute a malicious action)

- T1068: Exploitation for Privilege Escalation (use of the SYSTEM principal to escalate privileges)

## Additional Information:
This script must be run with administrator privileges.
The specified action path must exist.
The repeat interval must be at least 1 minute.
The principal must be either SYSTEM or ADMIN.
The script will create an output file in the user's home directory named current_context.txt containing the output of the whoami command.
