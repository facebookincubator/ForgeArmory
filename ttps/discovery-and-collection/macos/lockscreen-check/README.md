# Check if macOS Screen is Locked

![Community TTP - VVX7](https://img.shields.io/badge/Community_TTP-green)

This TTP leverages `ioreg` to determine if the macOS screen is locked.
If the screen is locked, attackers might execute GUI-altering actions,
like opening or closing windows.

## Pre-requisites

Ensure `ioreg` is available on the target system.

## Examples

Run the following to check the lock state of the macOS screen. The output
will confirm if the screen is either locked or unlocked:

```bash
ttpforge run forgearmory//discovery-and-collection/macos/lockscreen-check/lockscreen-check.yaml
```

## Steps

1. **Lockscreen Check**: Execute the `ioreg` command to determine
   the lock state of the macOS screen.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0007 Discovery
- **Techniques**:
  - T1016 System Network Configuration Discovery
