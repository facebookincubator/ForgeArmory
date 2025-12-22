# Load dylib via ssh-keygen

![Community TTP - VVX7](https://img.shields.io/badge/Community_TTP-green)

Loads a custom dylib (which opens Calculator) via ssh-keygen.

## Pre-requisites

Ensure that `gcc` is installed and that you have permission to run it.

## Examples

Execute `ssh-keygen -D` to load a dylib. Once execution is complete,
this TTP will delete the generated `calc.dylib` file if cleanup is
set to true:

```bash
ttpforge run forgearmory//defense-evasion/sshkeygen-dylib-hijack/ttp.yaml
```

## Steps

1. **Setup**: Compile the dylib that is loaded by ssh-keygen.

1. **Load Dylib**: Execute `ssh-keygen -D` to load the dylib.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0005 Defense Evasion
- **Techniques**:
  - T1574 Hijack Execution Flow
- **Subtechniques**:
  - T1574.002 Hijack Execution Flow: Dynamic Linker Hijacking
