# Red Canary osascript hidden dir rule trigger

## Description
This TTP tests a Red Canary detector to flag on osascript being executed against files in a hidden directory. It creates a hidden directory in /tmp, drops a JXA (JavaScript for Automation) file that runs the `whoami` command, and executes it via osascript.

## Arguments
This TTP takes no arguments.

## Requirements
- macOS (darwin) platform.

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/osascript-hiddendir/ttp.yaml
```

## Steps
1. **osascript_hiddendir**: Creates a hidden directory at /tmp/.purplehidden, drops a JXA script that executes `whoami` via shell, and runs it using osascript. The output is written to /tmp/osascript_hiddendir-execution.out. During cleanup, it removes the hidden directory and the output file.
