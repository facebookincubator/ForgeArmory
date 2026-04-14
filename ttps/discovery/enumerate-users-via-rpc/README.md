# Enumerate Active Directory Users via RPC

## Description
This TTP uses RPC to enumerate all Domain Users in an Active Directory domain.

## Arguments
- **host**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: The username for RPC authentication. Defaults to `NIL`.
- **password**: The password for the user. Defaults to `NIL`.

## Requirements
- Platform: Linux

## Example(s)
```bash
ttpforge run forgearmory//ttps/discovery/enumerate-users-via-rpc/ttp.yaml \
    --arg host=dc01.contoso.local \
    --arg username=admin \
    --arg password=P@ssw0rd
```

## Steps
1. **enumerate_domain_users**: Enumerate Active Directory usernames via RPC.
2. **enumerate_domain_admins**: Enumerate Active Directory Domain Admin usernames via RPC.
