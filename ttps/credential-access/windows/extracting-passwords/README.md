# Extracting Passwords with findstr

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP extracts credentials from files. Upon execution, the contents of files that contain the word "pass" will be displayed.

Derived from [Atomic Red Team T1552.001](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1552.001/T1552.001.md#atomic-test-4---extracting-passwords-with-findstr)

## Arguments
- **password**: a bool flag specifying the search be more granular and display files that contain the word 'password'

## Pre-requisites
- Windows operating system equipped with powershell

## Examples
You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//credential-access/windows/extracting-passwords/extracting-passwords.yaml
```
```bash
ttpforge run forgearmory//credential-access/windows/extracting-passwords/extracting-passwords.yaml --arg password=true
```

## Steps
1. **extract_cred_pass** : This step displays the contents of files that contain the word "pass" ("password" if argument is set to true)

## Manual Reproduction
```bash
#Displays the contents of files that contain the word "pass"

findstr /si pass *.xml *.doc *.txt *.xls

#Displays the contents of files that contain the word "password"

findstr /si password *.xml *.doc *.txt *.xls
```

## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0006 Credential Access
- **Techniques**:
    - T1552 Unsecured Credentials
- **Subtechniques**:
    - T1552.001 Credentials In Files
