# Golden Ticket Attack

## Description
Forges a Golden Ticket using Impacket's ticketer.py by leveraging a compromised krbtgt account hash.
Looks up the domain SID via lookupsid.py, then forges the ticket using the selected key type (RC4 or AES).

## Arguments
- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: Username for authentication to the domain controller (without domain prefix). No default (required).
- **password**: Password for authentication. No default (required).
- **ticket_type**: The type of krbtgt key to use for the golden ticket (rc4 or aes). RC4 uses an NT hash, AES uses an AES 128 or 256 bit key. Defaults to `rc4`.
- **krbtgt_key**: The krbtgt key to use (NT hash for RC4 or AES 128/256 bit key for AES). No default (required).
- **ticket_user**: The username to impersonate in the golden ticket. No default (required).
- **output_file**: Path to save the forged ticket file. Defaults to `/tmp/golden_ticket.ccache`.

## Requirements
- **Platforms:** Linux, macOS

## Example(s)
```bash
ttpforge run forgearmory//ttps/credential-access/forge-golden-ticket/ttp.yaml \
  --arg username=jsmith \
  --arg password='P@ssw0rd' \
  --arg krbtgt_key=aabbccdd11223344aabbccdd11223344 \
  --arg ticket_user=Administrator
```

## Steps
1. **setup_impacket**: Set up Python virtual environment with impacket.
2. **lookup_sid**: Look up the domain SID using lookupsid.py.
3. **extract_domain_sid**: Extract the domain SID from the lookupsid output.
4. **forge_golden_ticket**: Create a golden ticket for the target user using the specified key type. Cleanup removes the forged ticket file.
