# Enumerate Kerberoastable Users via LDAP

## Description
This TTP uses LDAP to enumerate Active Directory user accounts that are vulnerable
to Kerberoasting. Kerberoasting targets user accounts that have Service Principal
Names (SPNs) registered. An attacker can request TGS tickets for these accounts
and crack them offline to recover the service account password.

## Arguments
- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **bind_user**: The bind username in DOMAIN\user format for LDAP authentication. No default (required).
- **bind_password**: The password for the bind user. No default (required).
- **use_ldaps**: Use LDAPS (LDAP over SSL, port 636) instead of LDAP (port 389). Defaults to `false`.

## Requirements
- Platform: Linux, macOS

## Example(s)
```bash
ttpforge run forgearmory//ttps/discovery/enumerate-kerberoastable-users/ttp.yaml \
    --arg domain=contoso.local \
    --arg dc=dc01.contoso.local \
    --arg bind_user='CONTOSO\admin' \
    --arg bind_password=P@ssw0rd
```

## Steps
1. **enumerate_kerberoastable_users**: Enumerate Active Directory accounts vulnerable to Kerberoasting via LDAP search.
