# Regsvr32 local COM scriptlet execution

## Description
Abuses regsvr32.exe, a signed Microsoft binary, to execute malicious COM scriptlets in SCT files containing VBScript or JScript. Uses /s, /u, and /i parameters with scrobj.dll to execute malicious scriptlets without user prompts. This signed binary proxy execution technique evades application whitelisting.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **filename**: Name of the local file, include path (default: `./RegSvr32.sct`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/execute-com-scriptlet-regsvr32/ttp.yaml \
  --filename "C:\Payloads\malicious.sct"
```

## Steps
1. **ensure_scriptlet_exists**: Verifies that the SCT scriptlet file exists at the specified path before attempting execution. If the file is not found, the test exits with an error.
2. **execute_regsvr32_scriptlet**: Executes regsvr32.exe with the /s (silent), /u (unregister), and /i (install) parameters to load and execute the COM scriptlet file using scrobj.dll, which processes the script content and executes the embedded code.
