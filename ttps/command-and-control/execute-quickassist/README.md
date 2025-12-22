# Microsoft App Quick Assist Execution

## Description
Simulates adversary abuse of Microsoft Quick Assist, a legitimate remote support tool. Adversaries social engineer victims into launching the application and sharing connection codes, gaining remote access to execute commands and transfer files while appearing to use legitimate Microsoft software.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//command-and-control/execute-quickassist/ttp.yaml
```

## Steps
1. **execute_quick_assist**: Launches the Microsoft Quick Assist application using the Windows shell AppsFolder protocol.
