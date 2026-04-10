# GPO Discovery and Configuration Exfiltration

## Description

This chain TTP performs end-to-end Group Policy discovery and configuration exfiltration.

The attack chain:
1. Discovery: Enumerates GPOs via LDAP using enumerate-gpos-via-ldap
2. Exfiltration: Downloads GPO configurations from SYSVOL via SMB

## Arguments

- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: The username in DOMAIN\user format for LDAP/SMB authentication. Defaults to `CONTOSO\admin`.
- **password**: The password for the user. No default.
- **output_dir**: Directory to save downloaded GPO configurations. Defaults to `/tmp/gpo_configs`.

## Requirements

- Platform: Linux

## Example(s)

```bash
ttpforge run forgearmory//ttps/chains/gpo-discovery-and-download/ttp.yaml \
  --arg username='CONTOSO\admin' \
  --arg password=P@ssw0rd \
  --arg domain=contoso.local \
  --arg dc=dc01.contoso.local \
  --arg output_dir=/tmp/gpo_configs
```

## Steps

1. **enumerate_gpos**: Enumerate GPOs via LDAP to discover all Group Policy Objects in the domain.
2. **extract_gpo_guids**: Extract GPO GUIDs from the LDAP enumeration output.
3. **exfiltrate_gpo_configs**: Download GPO configurations from SYSVOL via SMB using the discovered GUIDs.
