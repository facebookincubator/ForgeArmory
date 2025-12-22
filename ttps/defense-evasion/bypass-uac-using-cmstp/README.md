# CMSTP Executing UAC Bypass

## Description
Bypasses UAC by abusing CMSTP.exe, a signed Microsoft binary that auto-elevates. Executes arbitrary commands embedded in specially crafted INF files without triggering UAC prompts. Leverages a legitimate Windows component for signed binary proxy execution.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **inf_file_uac**: Path to the INF file (default: `./T1218.003_uacbypass.inf`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/bypass-uac-using-cmstp/ttp.yaml \
  --inf_file_uac "C:\Temp\custom_bypass.inf"
```

## Steps
1. **ensure_inf_file_exists**: Verifies that the INF file exists at the specified path before attempting execution. If the INF file is not found, the test exits with an error.
2. **execute_cmstp_uac_bypass**: Executes CMSTP.exe with the /s (silent) and /au (auto-update) parameters to process the INF file and execute the embedded commands without displaying a user interface or triggering UAC prompts.
