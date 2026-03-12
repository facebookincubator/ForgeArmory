# Disable MDE Second Test

## Description
This TTP deletes the /Applications/Microsoft Defender.app directory and kills the running wdavdaemon process, which will stop MDE. It requires root privileges to execute successfully.

## Arguments
- **sleepval**: The number of seconds to sleep before restoring the Microsoft Defender.app directory during cleanup.

## Requirements
- Must be run with root/sudo privileges.

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/impair-mde-2/ttp.yaml --arg sleepval=60
```

## Steps
1. **removedir**: Checks if the current user is root, then makes a backup copy of the Microsoft Defender.app bundle, removes the original directory from /Applications, and kills the running wdavdaemon privileged process. During cleanup, it sleeps for the specified duration and restores the app bundle from the backup.
