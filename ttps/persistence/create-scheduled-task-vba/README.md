# Task Scheduler via VBA

## Description
Uses VBA macros in Office documents to create scheduled tasks via Windows Task Scheduler COM interfaces. Directly calls Windows API instead of utilities like schtasks.exe, bypassing command-line monitoring. Commonly observed in phishing campaigns for establishing persistence.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **ms_product**: Maldoc application Word (default: `Word`)
- **macro_file_path**: Path to macro code file (default: `./T1053.005-macrocode.txt`)
- **invoke_maldoc_path**: Path to Invoke-MalDoc.ps1 script (default: `./Invoke-MalDoc.ps1`)

## Requirements
1. Microsoft Office (specifically Microsoft Word) must be installed on the system
2. The Invoke-MalDoc.ps1 PowerShell script and macro code file must be present at the specified paths

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//persistence/create-scheduled-task-vba/ttp.yaml \
  --macro_file_path "C:\Payloads\scheduler-macro.txt" \
  --invoke_maldoc_path "C:\Tools\Invoke-MalDoc.ps1"
```

## Steps
1. **ensure_ms_office_installed**: Verifies that Microsoft Word is installed by attempting to create a Word COM object, then stops any running Word processes to ensure a clean execution environment. If Word is not installed, the test exits with an error.
2. **ensure_invoke_maldoc_exists**: Verifies that the Invoke-MalDoc.ps1 PowerShell script exists at the specified path before attempting execution. If the script is not found, the test exits with an error.
3. **ensure_macro_file_exists**: Verifies that the macro code file exists at the specified path before attempting to inject it. If the file is not found, the test exits with an error.
4. **execute_task_scheduler_via_vba**: Sources the Invoke-MalDoc.ps1 script and executes the Invoke-MalDoc function with the macro file to inject and execute the Task Scheduler VBA code within Word, calling the "Scheduler" subroutine from the macro to create the scheduled task.
