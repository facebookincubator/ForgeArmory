# Red Canary spctl rule trigger

## Description
This TTP tests a Red Canary detector that looks for spctl being executed against a file in /tmp. It creates a test file in /tmp and runs `spctl -a` against it to trigger the detection rule.

## Arguments
This TTP takes no arguments.

## Requirements
- macOS (darwin) platform.

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/spctl-trigger/ttp.yaml
```

## Steps
1. **spctl_trigger**: Creates a test file at /tmp/spctl-test.txt and executes `spctl -a /tmp/spctl-test.txt` to trigger the Red Canary detection rule. The exit code is suppressed since the goal is to generate the CLI string for detection. During cleanup, it removes the test file from /tmp.
