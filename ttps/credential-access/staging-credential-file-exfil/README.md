# Staging Popular Credential Files for Exfiltration

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP searches a drive for credential files used by the most common web browsers on Windows (Firefox, Chrome, Opera, and Edge), export the found files to a folder, and zip it, simulating how an adversary might stage sensitive credential files for exfiltration in order to conduct offline password extraction with tools like [firepwd.py](https://github.com/lclevy/firepwd) or [HackBrowserData](https://github.com/moonD4rk/HackBrowserData).

Derived from [Atomic Red Team T1555.003](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1555.003/T1555.003.md#atomic-test-10---stage-popular-credential-files-for-exfiltration)

## Arguments
- **exfil_folder**: a string flag specifying the destination location of the exfil folder. Default is "$env:temp\T1555.003".

## Pre-requisites
- Windows operating system equipped with powershell

## Examples
You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//credential-access/staging-credential-file-exfil/ttp.yaml
```
```bash
ttpforge run forgearmory//credential-access/staging-credential-file-exfil/ttp.yaml --arg exfil_folder=exfil
```


## Steps
1. **staging_cred_files_exfil** : This step adds a shortcut of the specified target executable to the current user's startup folder
2. **cleanup**: Removes the folder and zip hich contains the credential files

## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0006 Credential Access
- **Techniques**:
    - T1555 Credentials from Password Stores
- **Subtechniques**:
    - T1555.003 Credentials from Web Browsers
