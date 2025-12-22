# Open a local port through Windows Firewall to any profile

## Description
Opens network ports through Windows Firewall rules using netsh commands. Allows inbound TCP traffic on specified ports across all firewall profiles. Critical step in attack chains for establishing remote access, backdoor communications, data exfiltration, and lateral movement. Commonly observed in ransomware and APT campaigns.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **rule_name**: This is the name of the rule you wish to create (default: `Open Port to Any`)
- **local_port**: This is the local port you wish to test opening (default: `3389`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//utils/open-firewall-port/ttp.yaml \
  --rule_name "C2 Channel" \
  --local_port 4444
```

## Steps
1. **open_port_to_any_profile**: Uses netsh advfirewall firewall to create a new inbound firewall rule with the specified name that allows TCP traffic on the specified local port across all firewall profiles (Domain, Private, and Public).
