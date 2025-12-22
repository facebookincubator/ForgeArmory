# Visual Basic Script Execution to Gather Local Computer Information

## Description
Demonstrates VBScript execution via Windows Script Host (cscript.exe or wscript.exe) for system reconnaissance. Attackers use VBScript to gather system information, enumerate users/groups, and discover network configuration. The test executes a VBScript file using cscript.exe (console output) or wscript.exe (message boxes with 1-second timeout). Commonly observed in malware campaigns, phishing, and post-exploitation for intelligence gathering without deploying additional tools.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **method**: The method to execute VBA script (choices: `cscript`, `wscript`) (default: `cscript`)
- **vbscript_path**: Path to VBScript file (default: `./sys_info.vbs`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/execute-vbscript-with-script-engine/ttp.yaml \
  --method "wscript" \
  --vbscript_path "C:\Scripts\sysinfo.vbs"
```

## Steps
1. **ensure_vbscript_exists**: Verifies that the VBScript file exists at the specified path before attempting execution. If the file is not found, the test exits with an error.
2. **execute_script**: Executes the VBScript file using either cscript.exe (which outputs to the console) or wscript.exe (which uses message boxes with a 1-second timeout specified by //T:1 parameter) to gather and display system information, depending on the method argument.
