# DCSync krbtgt and Forge Golden Ticket

## Description

This chain TTP performs an end-to-end Golden Ticket attack by first extracting the
krbtgt account hash via DCSync, then using it to forge a Golden Ticket.

The attack chain:
1. Credential Access: DCSync the krbtgt account to extract its NT hash
2. Discovery: Look up the domain SID via lookupsid.py
3. Credential Access: Forge a Golden Ticket using the extracted krbtgt hash

## Arguments

- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: Username for authentication (without domain prefix). No default.
- **password**: Password for authentication. No default.
- **ticket_user**: The username to impersonate in the golden ticket. No default.
- **ticket_type**: The type of key to use for forging the ticket (`rc4` for NT hash, `aes` for AES-256 key). Choices: `rc4`, `aes`. Defaults to `rc4`.

## Requirements

- Platform: Linux or macOS

## Example(s)

```bash
ttpforge run forgearmory//ttps/chains/dcsync-and-forge-golden-ticket/ttp.yaml \
  --arg username=admin \
  --arg password=P@ssw0rd \
  --arg ticket_user=administrator \
  --arg domain=contoso.local \
  --arg dc=dc01.contoso.local
```

## Steps

1. **dcsync_krbtgt**: DCSync the krbtgt account to extract its NT hash.
2. **extract_krbtgt_hash**: Parse the krbtgt key (NT hash or AES-256 key) from the DCSync output.
3. **forge_golden_ticket**: Forge a Golden Ticket using the extracted krbtgt hash.
