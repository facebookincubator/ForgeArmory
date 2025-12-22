# Disable Windows Firewall

## Description
Disables Microsoft Defender Firewall using netsh command or registry modification. Removes a critical defensive layer, allowing malicious network communications to pass unfiltered. Commonly employed by malware for command and control, data exfiltration, or lateral movement.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **method**: The method to disable the firewall (choices: `netsh`, `registry`) (default: `netsh`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/disable-windows-firewall/ttp.yaml \
  --method "registry"
```

## Steps
1. **disable_firewall_netsh** (netsh method): Uses netsh advfirewall to set the current firewall profile state to off, disabling the firewall.
2. **disable_firewall_via_registry** (registry method): Modifies the EnableFirewall registry value in HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\PublicProfile, setting it to 0 to disable the firewall.
