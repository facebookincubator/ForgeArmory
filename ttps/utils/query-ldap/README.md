# Query LDAP

## Description
This TTP uses ldapsearch to perform LDAP queries against an Active Directory Domain.

## Arguments
- **domain**: The target Active Directory domain (e.g., contoso.com). No default (required).
- **dc**: The Domain Controller IP or hostname to target. No default (required).
- **bind_user**: The bind username in DOMAIN\\user format for LDAP authentication. No default (required).
- **bind_password**: The password for the bind user. No default (required).
- **search_filter**: The LDAP search filter to enumerate users. No default (required).
- **base_dn_prefix**: Optional prefix to prepend to the auto-generated base DN (e.g., CN=MicrosoftDNS,DC=DomainDnsZones for ADIDNS queries). Defaults to `NIL`.
- **result_limit**: The maximum number of results to return. Defaults to `50`.
- **use_ldaps**: Use LDAPS (LDAP over SSL, port 636) instead of LDAP (port 389). Defaults to `false`.
- **search_scope**: LDAP search scope - base, one, or sub. Defaults to `sub`.

## Requirements
- **Platforms:** Linux

## Example(s)
```bash
ttpforge run forgearmory//ttps/utils/query-ldap/ttp.yaml \
  --arg domain=contoso.local \
  --arg dc=dc01.contoso.local \
  --arg bind_user='CONTOSO\jsmith' \
  --arg bind_password='P@ssw0rd' \
  --arg search_filter='(objectClass=user)'
```

## Steps
1. **execute_ldap_query**: Execute ldapsearch to query LDAP. Automatically generates the base DN from the domain, applies optional prefix, and supports both LDAP and LDAPS protocols.
