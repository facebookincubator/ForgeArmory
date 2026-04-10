# DCSync Service Account and Forge Silver Ticket

## Description

This chain TTP performs an end-to-end Silver Ticket attack by first extracting a
service account's hash via DCSync, then using it to forge a Silver Ticket for that
service.

The attack chain:
1. Credential Access: DCSync the target service account to extract its NT hash
2. Discovery: Look up the domain SID via lookupsid.py
3. Credential Access: Forge a Silver Ticket using the extracted service account hash

Note: This chain does not include a command execution step because silver tickets
are service-specific -- the forged ticket is only valid for the exact service and
host matching the SPN. Use the forged ticket at /tmp/silver_ticket.ccache with the
appropriate Impacket client for your target service (e.g., mssqlclient.py for MSSQL,
smbclient.py for CIFS).

## Arguments

- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: Username for authentication (without domain prefix). No default.
- **password**: Password for authentication. No default.
- **target_user**: The sAMAccountName of the service account to DCSync and forge a ticket for. No default.
- **service_spn**: The Service Principal Name to forge the ticket for (e.g., cifs/server.domain.com). No default.
- **ticket_user**: The username to impersonate in the silver ticket. No default.
- **ticket_type**: The type of key to use for forging the ticket (`rc4` for NT hash, `aes` for AES-256 key). Choices: `rc4`, `aes`. Defaults to `rc4`.

## Requirements

- Platform: Linux or macOS

## Example(s)

```bash
ttpforge run forgearmory//ttps/chains/dcsync-and-forge-silver-ticket/ttp.yaml \
  --arg username=admin \
  --arg password=P@ssw0rd \
  --arg target_user=sqlsvc \
  --arg service_spn=MSSQLSvc/sql01.contoso.local:1433 \
  --arg ticket_user=administrator \
  --arg domain=contoso.local \
  --arg dc=dc01.contoso.local
```

## Steps

1. **dcsync_service_account**: DCSync the target service account to extract its NT hash.
2. **extract_service_hash**: Parse the service account key (NT hash or AES-256 key) from the DCSync output.
3. **forge_silver_ticket**: Forge a Silver Ticket using the extracted service account hash.
