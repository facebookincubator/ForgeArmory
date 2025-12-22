# Load Rootkit

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP simulates a rootkit by loading a Linux Kernel Module (LKM) and confirming it has loaded.

## Prerequisites

1. The executor must have root access on the system.

## Examples

```bash
ttpforge run forgearmory//defense-evasion/load-rootkit/ttp.yaml
```

## Steps

1. **compile-lkm**: This step compiles the kernel module.
2. **load-lkm**: This step loads the kernel module using the insmod command.
3. **check-success**: This step checks if the kernel module has loaded successfully by looking for the "LKM has loaded" string in the output of dmesg.

## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0005 Defense Evasion
- **Techniques**:
    - T1014 Rootkit
