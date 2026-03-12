# Red Canary rule trigger on open -a against /tmp

## Description
This TTP tests a Red Canary detector to flag on the `open -a` command being run against a file in the /tmp directory. This simulates suspicious execution behavior where an application is opened from a temporary directory.

## Arguments
This TTP takes no arguments.

## Requirements
- macOS (darwin) platform.

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/opentmp-trigger/ttp.yaml
```

## Steps
1. **opentmp_trigger**: Creates a test file at /tmp/pt-opentest.txt and executes `open -a /tmp/pt-opentest.txt` to trigger the Red Canary detector. The exit code is suppressed since the focus is on the CLI string rather than successful execution. During cleanup, it removes the test file from /tmp.
