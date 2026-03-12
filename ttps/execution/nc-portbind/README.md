# Netcat Port Binding

## Description
This TTP uses netcat to bind to a specified local port. It listens on the port using IPv6 for a configurable timeout period and then self-terminates. This simulates an attacker establishing a listening service on a compromised host.

## Arguments
- **port**: The port to bind to. Default: `8887`
- **timeout**: Timeout in seconds before the port bind self-terminates. Default: `900`

## Requirements
- Linux operating system

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/nc-portbind/ttp.yaml --arg port=9999 --arg timeout=300
```

## Steps
1. **nc_bind**: Use netcat (`nc -6 -lvvp`) to bind to the specified local port with IPv6 support. The binding self-terminates after the specified timeout period. No separate cleanup step is needed.
