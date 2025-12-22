# Tamper with Windows Defender Evade Scanning - Folder

## Description
Adds folder paths to Windows Defender's exclusion list, allowing malicious files within those directories to operate undetected. Significantly weakens endpoint protection effectiveness. Verify with: `(Get-MpPreference).ExclusionPath`.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **excluded_folder**: This folder will be excluded from scanning (default: `C:\Temp`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/add-defender-exclusion-path/ttp.yaml \
  --excluded_folder "C:\Users\Public\Downloads"
```

## Steps
1. **exclude_folder_from_scanning**: Adds the specified folder path to Windows Defender's exclusion list using the Add-MpPreference cmdlet with the -ExclusionPath parameter.
