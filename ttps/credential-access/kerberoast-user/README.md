# Kerberoasting Attack

## Description
Performs a Kerberoasting attack against a user with a Service Principal Name (SPN).
Uses Impacket's GetUserSPNs.py to request a TGS ticket and output a crackable hash.

## Arguments
- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: Username for authentication (without domain prefix). No default (required).
- **password**: Password for authentication. No default (required).
- **target_user**: The username of the service account to attack (without domain prefix). No default (required).

## Requirements
- **Platforms:** Linux, macOS

## Example(s)
```bash
ttpforge run forgearmory//ttps/credential-access/kerberoast-user/ttp.yaml \
  --arg username=jsmith \
  --arg password='P@ssw0rd' \
  --arg target_user=svc_mssql
```

## Steps
1. **setup_impacket**: Set up Python virtual environment with impacket.
2. **kerberoast**: Request TGS ticket for the target service account.
