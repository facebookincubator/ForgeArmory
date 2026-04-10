# Enumerate Active Directory Users via LDAP

## Description
This TTP uses LDAP to enumerate all Domain Users in an Active Directory domain.

## Arguments
- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **bind_user**: The bind username in DOMAIN\user format for LDAP authentication. No default (required).
- **bind_password**: The password for the bind user. No default (required).
- **use_ldaps**: Use LDAPS (LDAP over SSL, port 636) instead of LDAP (port 389). Defaults to `false`.

## Requirements
- Platform: Linux

## Example(s)
```bash
ttpforge run forgearmory//ttps/discovery/enumerate-users-via-ldap/ttp.yaml \
    --arg domain=contoso.local \
    --arg dc=dc01.contoso.local \
    --arg bind_user='CONTOSO\admin' \
    --arg bind_password=P@ssw0rd
```

## Steps
1. **enumerate_domain_users**: Enumerate Active Directory usernames via LDAP search.
2. **enumerate_domain_admins**: Enumerate Active Directory admin usernames via LDAP search (accounts with adminCount=1).
