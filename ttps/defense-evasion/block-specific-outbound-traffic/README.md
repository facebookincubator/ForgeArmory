# Blocking outbound traffic to specified port

## Description
This TTP modifies the macOS system firewall (`pf`) to block all outbound packets to a port specified by the user (default is 8443, commonly used by Velociraptor). It creates a backup of the firewall configuration, adds a blocking rule, makes the configuration file immutable, and restarts the firewall to apply the changes.

## Arguments
- **port_to_block**: The destination port to block for outbound traffic. Default: `8443`

## Requirements
- macOS (darwin) platform
- Root/sudo privileges required
- `pfctl` must be available

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/block-specific-outbound-traffic/ttp.yaml --arg port_to_block=443
```

## Steps
1. **Creating backup and updating firewall rules**: Creates a backup of `/etc/pf.conf`, appends a rule to block outbound TCP traffic to the specified port, verifies the updated rule, and sets the immutable flag on the configuration file.
2. **Restarting firewall to load new rules and dropping existing connections**: Displays current firewall rules, restarts `pfctl` to load the new configuration, displays the updated rules, and flushes existing connections. During cleanup, the immutable flag is removed, the modified configuration is deleted, the original backup is restored, and the firewall rules are reloaded.
