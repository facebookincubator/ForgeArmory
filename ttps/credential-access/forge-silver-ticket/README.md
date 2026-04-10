# Silver Ticket Attack

## Description
Forges a Silver Ticket using Impacket's ticketer.py by leveraging a compromised service account hash.
Looks up the domain SID via lookupsid.py, then forges a TGS ticket for a specific service
using the selected key type (RC4 or AES).

## Arguments
- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: Username for authentication to the domain controller (without domain prefix). No default (required).
- **password**: Password for authentication. No default (required).
- **ticket_type**: The type of service account key to use for the silver ticket (rc4 or aes). RC4 uses an NT hash, AES uses an AES 128 or 256 bit key. Defaults to `rc4`.
- **service_key**: The service account key to use (NT hash for RC4 or AES 128/256 bit key for AES). No default (required).
- **service_spn**: The Service Principal Name to forge the ticket for (e.g., cifs/server.domain.com). No default (required).
- **ticket_user**: The username to impersonate in the silver ticket. No default (required).
- **output_file**: Path to save the forged ticket file. Defaults to `/tmp/silver_ticket.ccache`.

## Requirements
- **Platforms:** Linux, macOS

## Example(s)
```bash
ttpforge run forgearmory//ttps/credential-access/forge-silver-ticket/ttp.yaml \
  --arg username=jsmith \
  --arg password='P@ssw0rd' \
  --arg service_key=aabbccdd11223344aabbccdd11223344 \
  --arg service_spn=cifs/fileserver.contoso.local \
  --arg ticket_user=Administrator
```

## Steps
1. **setup_impacket**: Set up Python virtual environment with impacket.
2. **lookup_sid**: Look up the domain SID using lookupsid.py.
3. **extract_domain_sid**: Extract the domain SID from the lookupsid output.
4. **forge_silver_ticket**: Create a silver ticket for the target service using the specified key type. Cleanup removes the forged ticket file.
