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
ttpforge run forgearmory//defense-evasion/macos/disable-system-updates/disable-system-updates.yaml
```

## Steps

1. **Disable Updates**: Execute defaults to disable automatic system security
   updates.

1. **Cleanup**: If the `cleanup` argument is set to `true`, execute defaults
   to enable automatic system security updates.

mitre:
  tactics:
    - TA0003 Persistence
  techniques:
    - T1543 Create or Modify System Process
  subtechniques:
    - "T1543.001 Create or Modify System Process: Launch Agent"
