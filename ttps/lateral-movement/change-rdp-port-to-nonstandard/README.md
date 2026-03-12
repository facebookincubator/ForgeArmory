# Changing RDP Port to Non Standard Port via Powershell

## Description
Changes RDP listening port from default 3389 to non-standard port to evade detection and bypass firewall rules. Modifies PortNumber registry value and creates new firewall rule. Commonly observed in APT campaigns for establishing covert remote access channels.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **old_remote_port**: Default RDP Listening Port (default: `3389`)
- **new_remote_port**: New RDP Listening Port (default: `4489`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//lateral-movement/change-rdp-port-to-nonstandard/ttp.yaml \
  --new_remote_port "5555"
```

## Steps
1. **change_rdp_port**: Modifies the PortNumber registry value in the RDP-Tcp configuration to change the RDP listening port to the specified new port, then creates a new Windows Firewall rule named "RDPPORTLatest-TCP-In" to allow inbound TCP connections on the new port.
