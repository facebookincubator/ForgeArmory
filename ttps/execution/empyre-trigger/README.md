# Red Canary python empyre command line string detector test

## Description
This TTP tests a Red Canary detector that flags on a specific command observed with python empyre. It runs an ifconfig command filtering for inet addresses excluding localhost, which matches a known empyre reconnaissance pattern.

## Arguments
This TTP takes no arguments.

## Requirements
- macOS (darwin) platform.

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/empyre-trigger/ttp.yaml
```

## Steps
1. **empyre_trigger**: Executes `ifconfig | grep inet | grep -v 127.0.0.1` to mimic a command line string observed in python empyre malware for network reconnaissance. No cleanup is needed for this TTP.
