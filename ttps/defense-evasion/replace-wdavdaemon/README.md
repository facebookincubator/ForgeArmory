# replace_wdavdaemon

## Description
This TTP replaces the wdavdaemon binary with a dummy script to impair MDE. It backs up the original binary, replaces it with a script that writes to a file in /tmp when invoked, and sets the immutable bit to prevent overwriting. After a configurable timeout, the original binary is restored during cleanup.

## Arguments
- **timeout**: Time in seconds before starting the cleanup routine. Default: `30`.

## Requirements
- macOS (darwin) platform.
- Must be run with superuser (root) privileges.

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/replace-wdavdaemon/ttp.yaml --arg timeout=60
```

## Steps
1. **replace_binary**: Backs up the original wdavdaemon binary, replaces it with a shell script that logs to /tmp/wdavout.txt, and sets the system immutable flag (`schg`) on the replacement to prevent configuration management from overwriting it. Sleeps for the specified timeout period. During cleanup, it removes the immutable flag, restores the original binary, and cleans up temporary files.
