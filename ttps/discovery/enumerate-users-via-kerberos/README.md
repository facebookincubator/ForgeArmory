# Enumerate Active Directory Users via Kerberos

## Description
This TTP enumerates valid usernames in the given Active Directory domain
by sending Kerberos AS-REQ messages without pre-authentication data.
This technique does not transmit passwords, does not generate failed logon
events, and carries no account-lockout risk.

## Arguments
- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **userlist**: Path to the wordlist containing usernames to enumerate. Defaults to `users.txt`.

## Requirements
- Platform: Linux, macOS

## Example(s)
```bash
ttpforge run forgearmory//ttps/discovery/enumerate-users-via-kerberos/ttp.yaml \
    --arg domain=contoso.local \
    --arg dc=dc01.contoso.local \
    --arg userlist=users.txt
```

## Steps
1. **setup_impacket**: Set up Python virtual environment with impacket.
2. **enumerate_users**: Enumerate valid Active Directory usernames via Kerberos pre-authentication.
