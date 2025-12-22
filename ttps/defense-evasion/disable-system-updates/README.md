# Disable System Security Updates

![Community TTP - VVX7](https://img.shields.io/badge/Community_TTP-green)

Disable automatic system security updates.

## Pre-requisites

Ensure that you have the necessary permissions to write to
`/Library/Preferences/com.apple.SoftwareUpdate.plist`.

## Examples

Execute defaults to disable macOS system security updates. Once execution is
complete, this TTP will re-enable automatic system security updates if cleanup
is set to true:

```bash
ttpforge run forgearmory//defense-evasion/disable-system-updates/ttp.yaml
```

## Steps

1. **Disable Updates**: Execute defaults to disable automatic system security
   updates. Unless `--no-cleanup` is set, the settings required to
   enable automatic system security updates will be re-enabled.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0005 Defense Evasion
- **Techniques**:
  - T1562 Impair Defenses
- **Subtechniques**:
  - T1562.001 Impair Defenses: Disable or Modify Tools
