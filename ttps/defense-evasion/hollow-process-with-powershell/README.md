# Process Hollowing using PowerShell

## Description
Demonstrates process hollowing, an advanced code injection technique where a legitimate process is created suspended, its memory unmapped, and replaced with malicious code. The malicious code runs under the name and PID of the legitimate executable, evading detection. Uses PowerShell implementation based on FuzzySecurity's Start-Hollow script.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **script_path**: Path to Start-Hollow.ps1 script (default: `./Start-Hollow.ps1`)
- **hollow_binary_path**: Path of the binary to hollow (executable that will run inside the sponsor) (default: `C:\Windows\System32\cmd.exe`)
- **parent_process_name**: Name of the parent process (default: `explorer`)
- **sponsor_binary_path**: Path of the sponsor binary (executable that will host the binary) (default: `C:\Windows\System32\notepad.exe`)
- **spawnto_process_name**: Name of the process to spawn (default: `notepad`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/hollow-process-with-powershell/ttp.yaml \
  --script_path "C:\Tools\Start-Hollow.ps1" \
  --sponsor_binary_path "C:\Windows\System32\calc.exe"
```

## Steps
1. **ensure_script_exists**: Verifies that the Start-Hollow.ps1 PowerShell script exists at the specified path before attempting execution. If the script is not found, the test exits with an error.
2. **execute_process_hollowing**: Sources the Start-Hollow.ps1 script, retrieves the process ID of the specified parent process (explorer by default), and executes the Start-Hollow function with verbose output to create a hollowed process where the sponsor binary hosts the hollow binary under the specified parent process.
