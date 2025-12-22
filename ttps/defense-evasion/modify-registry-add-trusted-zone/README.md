# Add domain to Trusted sites Zone

## Description
Adds malicious domains to Internet Explorer's Trusted Sites Zone (Zone 2) through registry modifications. This relaxes security restrictions and enables C2 communications without triggering security warnings. Documented in attacks abusing Office 365 PowerShell for covert C2.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **bad_domain**: Domain to add to trusted site zone (default: `bad-domain.com`)
- **backup_location**: Path where registry backup will be saved (default: `C:\Users\Public\backup.reg`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/modify-registry-add-trusted-zone/ttp.yaml \
  --bad_domain "malicious-c2.com" \
  --backup_location "C:\Temp\zonemap_backup.reg"
```

## Steps
1. **backup_registry**: Exports the current Internet Settings ZoneMap registry configuration from HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap to a backup file for restoration during cleanup.
2. **add_trusted_site**: Creates a new registry key for the specified domain and a subdomain named "bad-subdomain", then sets DWORD values of 2 (Trusted Sites Zone) for https, http, and wildcard (*) protocols to add the domain to the Trusted Sites Zone.
