# Red Canary installcore rule trigger

## Description
This TTP tests a Red Canary detector to flag on the /Volumes/Installer/Installer.app/Contents/MacOS/sonorus command line string being found. The detector should trigger based on the CLI arguments even if the InstallCore malware is not present on the system.

## Arguments
This TTP takes no arguments.

## Requirements
- macOS (darwin) platform.

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/installcore-trigger/ttp.yaml
```

## Steps
1. **installcore_trigger**: Attempts to execute the path `/Volumes/Installer/Installer.app/Contents/MacOS/sonorous` with a test argument. The command is expected to fail since the malware binary is not present, but the CLI string itself should trigger the Red Canary detector. No cleanup is needed.
