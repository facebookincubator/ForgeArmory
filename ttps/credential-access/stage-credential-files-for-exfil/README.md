# Stage Popular Credential Files for Exfiltration

## Description
Searches a drive for credential files used by the most common web browsers on Windows (Firefox, Chrome, Opera, and Edge), exports the found files to a folder, and compresses them into a zip archive. This simulates how an adversary might stage sensitive credential files for exfiltration in order to conduct offline password extraction with tools like [firepwd.py](https://github.com/lclevy/firepwd) or [HackBrowserData](https://github.com/moonD4rk/HackBrowserData).

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **exfil_folder**: Destination location for the exfiltration folder (default: `$env:temp\T1555.003`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//credential-access/stage-credential-files-for-exfil/ttp.yaml \
  --exfil_folder "C:\Temp\staged_creds"
```

## Steps
1. **staging_cred_files_exfil**: Creates the exfiltration directory if it doesn't exist, searches for and copies credential files from Firefox, Chrome, Opera, and Edge browsers, then compresses all staged files into a zip archive.
