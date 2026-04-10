# DCSync Attack

## Description
Performs a DCSync attack to replicate credentials from a Domain Controller.
Uses Impacket's secretsdump.py to request replication of a target user's
password hashes via the MS-DRSR (Directory Replication Service Remote) protocol.

## Arguments
- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: Username for authentication (without domain prefix). No default (required).
- **password**: Password for authentication. No default (required).
- **target_user**: The username of the account to dump credentials for (without domain prefix). No default (required).
- **auth_method**: Authentication method to use (kerberos or ntlm). Defaults to `ntlm`.

## Requirements
- **Platforms:** Linux, macOS

## Example(s)
```bash
ttpforge run forgearmory//ttps/credential-access/dcsync-user/ttp.yaml \
  --arg username=jsmith \
  --arg password='P@ssw0rd' \
  --arg target_user=krbtgt
```

```bash
ttpforge run forgearmory//ttps/credential-access/dcsync-user/ttp.yaml \
  --arg username=jsmith \
  --arg password='P@ssw0rd' \
  --arg target_user=Administrator \
  --arg auth_method=kerberos
```

## Steps
1. **setup_impacket**: Set up Python virtual environment with impacket.
2. **dcsync**: Perform DCSync to replicate target user credentials. Supports both NTLM and Kerberos authentication methods.
