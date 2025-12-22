# Command prompt writing script to file then executes it

## Description
Creates and executes VBScript files on-the-fly using cmd.exe echo commands. Simulates DarkGate malware behavior. Maintains smaller footprint on disk and bypasses security controls monitoring for pre-existing malicious files.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **script_path**: Path in which the script will be written (default: `C:\Users\Public`)
- **script_name**: Script name (without the extension) (default: `AtomicTest`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/create-and-execute-vbscript/ttp.yaml \
  --script_path "C:\Temp" \
  --script_name "SystemCheck"
```

## Steps
1. **write_and_execute_vbscript**: Changes directory to the specified script path, uses echo to write VBScript code that creates a WScript.Shell object and executes the whoami command, saves it to a .vbs file, and immediately executes the VBScript file.
