# Terminal Server Client Connection History Cleared

## Description
Clears RDP connection history from the Windows Registry (HKCU:\SOFTWARE\Microsoft\Terminal Server Client) to cover tracks and evade detection. Removes evidence of lateral movement, making incident response and forensic investigations more difficult.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/clear-rdp-connection-logs/ttp.yaml
```

## Steps
1. **ensure_rdp_history_exists**: Verifies that RDP connection history exists in the registry, and if not, creates sample registry entries including a default connection to 127.0.0.1 and a server entry named "Redcanary" to ensure there is history to clear.
2. **clear_rdp_history**: Deletes all values in the Default registry key and removes the entire Servers registry key to clear all RDP connection history from the system.
