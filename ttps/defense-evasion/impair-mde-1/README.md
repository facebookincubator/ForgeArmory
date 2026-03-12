# Disable MDE

## Description
This TTP simply unloads the com.microsoft.fresno.plist launch daemon to disable MDE instantly. It requires root privileges to execute successfully.

## Arguments
- **sleepval**: The number of seconds to sleep before reloading the com.microsoft.fresno.plist launch daemon during cleanup.

## Requirements
- Must be run with root/sudo privileges.

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/impair-mde-1/ttp.yaml --arg sleepval=60
```

## Steps
1. **unloadplist**: Checks if the current user is root, then unloads the com.microsoft.fresno.plist launch daemon using `launchctl unload`. Creates a canary file to track successful execution. During cleanup, it sleeps for the specified duration and then reloads the plist to restore MDE.
