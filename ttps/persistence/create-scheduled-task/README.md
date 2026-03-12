# Create Scheduled Task for Persistence

![Persistence TTP](https://img.shields.io/badge/Persistence_TTP-blue)

This TTP (Tactic, Technique, and Procedure) is designed to create a
scheduled task in Windows for persistence. It defaults to running
`calc.exe` if no command or path is provided, but can be configured for
any executable or script.

## Arguments

- **taskname**: Name of the scheduled task.

  Default: ttpforge-persistence

- **workdir**: Working directory for the task.

  Default: "C:\\Users\\Public"

- **task_file**: Name of the batch file for persistence.

  Default: "Persist.bat"

- **tasktime**: Time to run the scheduled task.

  Default: "06:00"

- **searchstring**: String to search for in task creation events.

  Default: "ttpforge-persistence"

- **command_or_path**: Command or path to the executable.

  Default: "calc.exe"

- **detect**: Boolean flag to enable detection.

  Default: true

## Pre-requisites

1. Windows operating system with sufficient permissions to create
   scheduled tasks.

2. PowerShell for executing the script steps.

3. Command Prompt access for additional scripting and cleanup.

## Examples

To run this TTP, use a command like the following, adjusting arguments
as needed:

```powershell
.\ttpforge.exe run forgearmory//persistence/create-scheduled-task/ttp.yaml
```

Example to specify a custom task name and time:

```powershell
.\ttpforge.exe run forgearmory//persistence/create-scheduled-task/ttp.yaml \
  --arg taskname=myTask \
  --arg tasktime="08:00"
```

## Steps

1. **create-scheduled-task**: Creates a batch script and sets up the
   scheduled task using PowerShell.

2. **run-scheduled-task**: Executes the scheduled task immediately and
   handles cleanup with a batch script.

3. **check-task-creation**: Verifies the creation of the scheduled task
   using PowerShell.

4. **check-detection**: Checks for detection of the task creation event
   using Command Prompt and cleanup with PowerShell.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence

- **Techniques**:
  - T1053 Scheduled Task/Job
