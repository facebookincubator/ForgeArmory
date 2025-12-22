# WinPwn - Loot local Credentials - Invoke-WCMDump

## Description
Extracts stored credentials from Windows Credential Manager using the Invoke-WCMDump PowerShell function. Credential Manager stores authentication credentials for websites, applications, and network resources.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **script_path**: Path to DumpWCM.ps1 script file (default: `./Invoke-WCMDump.ps1`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//credential-access/dump-windows-credential-manager/ttp.yaml \
  --script_path "C:\Tools\Invoke-WCMDump.ps1"
```

## Steps
1. **ensure_script_exists**: Verifies that the DumpWCM script exists at the specified path before attempting execution. If the script is not found, the test exits with an error.
2. **invoke_wcm_dump**: Sources the Invoke-WCMDump script and executes the Invoke-WCMDump function to dump credentials from Windows Credential Manager.
