# Execute VBScript with Signed Binary

## Description
Executes VBScript commands using signed Microsoft binaries (mshta.exe or rundll32.exe) to evade detection. This trusted binary proxy execution technique has been observed in FIN7 campaigns to bypass application whitelisting and EDR solutions.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **method**: The method to execute VBScript (choices: `mshta`, `rundll32`) (default: `mshta`)
- **command_to_execute**: Command to execute (default: `calc.exe`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/execute-vbscript-signed-binary/ttp.yaml \
  --method "rundll32" \
  --command_to_execute "notepad.exe"
```

## Steps
1. **execute_mshta_vbscript** (mshta method only): Uses mshta.exe with the vbscript: protocol to execute inline VBScript code that creates a WScript.Shell object and uses its Run method to launch PowerShell with the specified command, then immediately closes the HTML application window.
2. **execute_vbscript_command** (rundll32 method only): Uses rundll32.exe to load vbscript: with mshtml and execute VBScript code that creates a WScript.Shell object to run the specified command, providing an alternative signed binary proxy execution method.
