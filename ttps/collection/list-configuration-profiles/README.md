# List macOS Configuration Profiles

![Community TTP - VVX7](https://img.shields.io/badge/Community_TTP-green)

This TTP enumerates all configuration profile names using the `profiles`
binary. It helps attackers identify what configuration profiles are
installed on the target host.

## Pre-requisites

Ensure the `profiles` binary is available on the target macOS system.

## Examples

Run the following to list all configuration profiles on the macOS system.
After execution, you will see a list of installed configuration profiles:

```bash
ttpforge run forgearmory//collection/list-configuration-profiles/ttp.yaml
```

## Steps

1. **List Configuration Profiles**: Execute the `profiles` command to
   enumerate the configuration profiles on the macOS system.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0009 Collection
- **Techniques**:
  - T1602 Data From Configuration Repository
