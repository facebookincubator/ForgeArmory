# macOS Get Running Processes

![Community TTP - VVX7](https://img.shields.io/badge/Community_TTP-green)

Utilize ps to view currently running processes.

## Pre-requisites

Ensure that ps is installed on the target system and that you have the necessary
permissions to run it.

## Examples

Utilize ps to view currently running processes. This TTP does not produce
artifacts, so it is not necessary to run the clean up afterward:

```bash
ttpforge run ttps/discovery/macos/get-running-processes/get-running-processes.yaml
```

## Steps

1. **Run PS**: Execute ps to view currently running processes.
