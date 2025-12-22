# Disable NLA for RDP via Command Prompt

## Description
Disables Network Level Authentication (NLA) for RDP through registry modification. Allows attackers to interact with Windows sign-in screen before authentication, enabling password guessing and authentication bypass vulnerabilities. Observed in Flax Typhoon APT campaigns targeting Taiwanese organizations.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//lateral-movement/disable-nla-for-rdp/ttp.yaml
```

## Steps
1. **disable_nla_for_rdp**: Uses the reg add command to modify the UserAuthentication registry value in the RDP-Tcp configuration, setting it to 0 (DWORD) to disable Network Level Authentication for RDP connections.
