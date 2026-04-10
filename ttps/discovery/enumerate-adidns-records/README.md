# Enumerate ADIDNS Records via LDAP

## Description
This TTP enumerates Active Directory-Integrated DNS (ADIDNS) records via LDAP.
It queries DNS zones and records stored in AD DNS partitions, extracting
hostnames and IP addresses to discover machines in the domain.

## Arguments
- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **bind_user**: The bind username in DOMAIN\user format for LDAP authentication. No default (required).
- **bind_password**: The password for the bind user. No default (required).
- **dns_partition**: DNS partition: domain, forest, or legacy. Defaults to `legacy`.
- **use_ldaps**: Use LDAPS (port 636) instead of LDAP (port 389). Defaults to `false`.

## Requirements
- Platform: Linux

## Example(s)
```bash
ttpforge run forgearmory//ttps/discovery/enumerate-adidns-records/ttp.yaml \
    --arg domain=contoso.local \
    --arg dc=dc01.contoso.local \
    --arg bind_user='CONTOSO\admin' \
    --arg bind_password=P@ssw0rd \
    --arg dns_partition=legacy
```

## Steps
1. **enumerate_dns_records**: Enumerate DNS records in the domain zone via LDAP query.
2. **parse_dns_records**: Parse dnsRecord data to extract hostnames and IPs from the LDAP results.
