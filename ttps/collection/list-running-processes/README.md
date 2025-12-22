# macOS Get Running Processes

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

Utilize `ps` to view currently running processes.

## Pre-requisites

Ensure that `ps` is installed on the target system and that you have the necessary
permissions to run it.

## Examples

Utilize `ps` to view currently running processes. This TTP does not produce
artifacts, so it is not necessary to run the clean up afterward:

```bash
ttpforge run forgearmory//collection/list-running-processes/ttp.yaml
```

## Steps

1. **Run PS**: Execute `ps` to view currently running processes.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0009 Collection
- **Techniques**:
  - T1057 Process Discovery
