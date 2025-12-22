# Drop Suspicious File and Display It

## Description
Demonstrates file dropping to disk using Windows Command Shell. Uses echo to write content to a file and type to display contents, simulating malware that stages payloads and verifies them. Attackers use native commands like echo because they're present on all systems, avoid triggering antivirus alerts, and integrate easily into scripts. The .bin extension simulates suspicious binary or data files.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **file_contents_path**: Path to the file that the command prompt will drop (default: `C:\Users\Public\test.bin`)
- **message**: Message that will be written to disk and then displayed (default: `Hello from the Windows Command Prompt!`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/drop-suspicious-file-and-display/ttp.yaml \
  --file_contents_path "C:\Temp\payload.dat" \
  --message "Malicious payload content here"
```

## Steps
1. **write_and_display_file**: Uses the echo command to write the specified message to a file, then uses the type command to display the file's contents to verify successful file creation.
