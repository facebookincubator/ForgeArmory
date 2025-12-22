# Create and Execute Batch Script

## Description
Demonstrates batch script creation and execution on Windows for command automation. Attackers use batch scripts for reconnaissance, data collection, lateral movement, persistence, and payload execution because they're native to Windows, require no additional software, and are easily obfuscated. The test creates a script with a specified command (default: `dir`) and executes it. CMD briefly launches then closes, enabling background execution. Commonly observed in malware droppers, post-exploitation frameworks, and automated attack chains.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **command_to_execute**: Command to execute within script (default: `dir`)
- **script_path**: Path to batch script file (default: `C:\Users\Public\T1059.003_script.bat`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/create-and-execute-batch-script/ttp.yaml \
  --command_to_execute "whoami" \
  --script_path "C:\Temp\recon.bat"
```

## Steps
1. **ensure_script_exists**: Creates a new batch script file if it doesn't exist, then writes the specified command to the script file using PowerShell's Set-Content cmdlet.
2. **execute_batch_script**: Uses Start-Process to execute the batch script file, which launches a new cmd.exe process to run the commands contained in the script.
