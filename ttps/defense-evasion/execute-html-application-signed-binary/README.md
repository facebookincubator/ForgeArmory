# Execute HTML Application (HTA) with Signed Binary

## Description
Executes HTML Application (HTA) files using signed Microsoft binaries (mshta.exe or rundll32.exe with url.dll). This trusted binary proxy execution technique evades application whitelisting and has been observed in IcedID and Trickbot malware campaigns.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **method**: The method to execute HTA file (choices: `mshta`, `rundll32`) (default: `mshta`)
- **hta_file_path**: Path to HTA file for execution (default: `./index.hta`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/execute-html-application-signed-binary/ttp.yaml \
  --method "rundll32" \
  --hta_file_path "C:\Payloads\malicious.hta"
```

## Steps
1. **ensure_hta_exists**: Verifies that the HTA file exists at the specified path before attempting execution. If the file is not found, the test exits with an error.
2. **execute_hta_mshta** (mshta method only): Executes the HTA file using mshta.exe, which launches the HTML Application Host to process and run the HTA content.
3. **execute_hta_rundll32** (rundll32 method only): Executes the HTA file using rundll32.exe with the url.dll library and OpenURL function, which provides an alternative signed binary proxy execution method for running HTA files.
