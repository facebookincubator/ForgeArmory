# Execute JavaScript with Script Engine

## Description
Executes JavaScript code using Windows Script Host engines (cscript.exe or wscript.exe). This native Windows capability is commonly used by attackers for command execution and system reconnaissance without requiring additional software installation.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **method**: The method to execute JavaScript (choices: `cscript`, `wscript`) (default: `cscript`)
- **jscript_path**: Path to sample JScript file (default: `./sys_info.js`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/execute-javascript-with-script-engine/ttp.yaml \
  --method "wscript" \
  --jscript_path "C:\Scripts\recon.js"
```

## Steps
1. **ensure_jscript_exists**: Verifies that the JavaScript file exists at the specified path before attempting execution. If the file is not found, the test exits with an error.
2. **execute_javascript**: Executes the JavaScript file using either cscript.exe (which outputs to the console) or wscript.exe (which uses message boxes with a 1-second timeout specified by //T:1 parameter), depending on the method argument.
