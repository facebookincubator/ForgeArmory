# Enumerate Active Directory via DNS SRV Records

## Description
This TTP uses dig to query DNS SRV records for Active Directory service discovery.
It enumerates Domain Controllers, Global Catalog servers, Kerberos KDCs, and other
AD-related services by querying standard AD DNS SRV records.
If no host is specified, queries are sent to the system's default DNS resolver.

## Arguments
- **domain**: The target Active Directory domain / default naming context (e.g., contoso.com). Defaults to `contoso.local`.
- **host**: The Domain Controller IP or hostname to query DNS against. Defaults to `dc01.contoso.local`.

## Requirements
- Platform: Linux

## Example(s)
```bash
ttpforge run forgearmory//ttps/discovery/enumerate-computers-via-dns/ttp.yaml \
    --arg domain=contoso.local \
    --arg host=dc01.contoso.local
```

## Steps
1. **enumerate_ldap_servers**: Query SRV records for LDAP servers hosting the domain.
2. **enumerate_domain_controllers**: Query SRV records for Domain Controllers.
3. **enumerate_pdc**: Query SRV records for PDC Emulator.
4. **enumerate_global_catalog**: Query SRV records for Global Catalog servers.
5. **enumerate_kerberos_kdc**: Query SRV records for Kerberos KDC over TCP and UDP.
6. **enumerate_kerberos_dc**: Query SRV records for DCs running KDC over TCP.
7. **enumerate_kpasswd**: Query SRV records for Kerberos password change over TCP and UDP.
