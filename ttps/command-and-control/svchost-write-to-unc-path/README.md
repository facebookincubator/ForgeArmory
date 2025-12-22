# svchost writing a file to a UNC path

## Description
Demonstrates suspicious behavior where masqueraded svchost.exe writes files to UNC paths. Copies cmd.exe and renames it as svchost.exe, then writes to network share via UNC path. Adversaries use this to evade detection or transfer files to network shares.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//command-and-control/svchost-write-to-unc-path/ttp.yaml
```

## Steps
1. **svchost_unc_write**: Copies cmd.exe to C:\svchost.exe to masquerade as the legitimate svchost process, then executes it to write "T1105" to a UNC path (\\localhost\c$\T1105.txt).
