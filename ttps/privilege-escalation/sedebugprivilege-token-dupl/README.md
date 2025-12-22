# "SeDebugPrivilege" Token Duplication

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP uses PowerShell and a modified version of Empire's [GetSystem module](https://github.com/BC-SECURITY/Empire/blob/v3.4.0/data/module_source/privesc/Get-System.ps1).
The modified script uses `SeDebugPrivilege` to obtain, duplicate and impersonate the token of a another process.
When executed successfully, the test displays the domain and name of the account it's impersonating (local SYSTEM).

Derived from [Atomic Red Team T1134.001](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1134.001/T1134.001.md#atomic-test-2---sedebugprivilege-token-duplication)

## Arguments
- **script**: a string variable specifying location of Get-System.ps1 script. Default is $PWD\src\Get-System.ps1

## Pre-requisites
- Windows operating system equipped with powershell

## Examples
You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//collection/windows/privilege-escalation/sedebugprivilege-token-dupl.yaml
```
```bash
ttpforge run forgearmory//collection/windows/privilege-escalation/sedebugprivilege-token-dupl.yaml --arg Get-System-mod.ps1
```

## Steps
1. **execute_script** : This step executes the script which obtain, duplicate and impersonate the token of a another process.

    Note: cleanup --> TTP user is responsible for cleanup by removing Get-System.ps1 manually

## Manual Reproduction
```bash
#Commands to execute the script
IEX (Get-Content "src\Get-System.ps1" -Raw); Get-System -Technique Token
Start-Sleep -Second 3
IEX (Get-Content "src\Get-System.ps1" -Raw); Get-System -RevToSelf
```

## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0004 Privilege Escalation
- **Techniques**:
    - T1134 Access Token Manipulation
- **Subtechniques**:
    - T1134.003 Make and Impersonate Token
