# AS-REP Roasting Attack

## Description
Performs an AS-REP Roasting attack against a user with Kerberos pre-authentication disabled.
Uses Impacket's GetNPUsers.py to request an AS-REP ticket and output a crackable hash.

## Arguments
- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **target_user**: The username of the vulnerable account to attack (without domain prefix). No default (required).

## Requirements
- **Platforms:** Linux, macOS

## Example(s)
```bash
ttpforge run forgearmory//ttps/credential-access/asrep-roast-user/ttp.yaml \
  --arg target_user=svc_backup
```

## Steps
1. **setup_impacket**: Set up Python virtual environment with impacket.
2. **asrep_roast**: Request AS-REP ticket for the target user.
