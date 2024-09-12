# Executable Shortcut Link to User Startup Folder

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP adds a non-malicious executable shortcut link to the current user's startup directory.
Test can be verified by going to the users startup directory and checking if the shortcut link exists.

Derived from [Atomic Red Team T1547.001](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1547.001/T1547.001.md#atomic-test-7---add-executable-shortcut-link-to-user-startup-folder)

## Arguments
- **shortcut**:  a string flag specifying the shortcut link name. Default is "calc_exe".
- **target**: a path flag specifying the target executable. Default is "C:\Windows\System32\calc.exe".

## Pre-requisites
- Windows operating system equipped with powershell

## Examples
You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//persistence/windows/add-shortcut-startup/add-shortcut-startup.yaml
```
```bash
ttpforge run forgearmory//persistence/windows/add-shortcut-startup/add-shortcut-startup.yaml --arg shortcut=shortcutTest
```
```bash
ttpforge run forgearmory//persistence/windows/add-shortcut-startup/add-shortcut-startup.yaml --arg target=C:\Windows\System32\test.exe
```


## Steps
1. **add_exe_shortcut** : This step adds a shortcut of the specified target executable to the current user's startup folder
2. **cleanup**: Removes the shortcut link from user's startup folder

## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0003 Persistence / TA0004 Privilege Escalation
- **Techniques**:
    - T1547 Boot or Logon Autostart Execution
- **Subtechniques**:
    - T1547.001 Registry Run Keys / Startup Folder
