# Retrieve DPAPI Backup Key from Domain Controller

## Description
Retrieves the DPAPI domain backup key from a Domain Controller over RPC using
Impacket's dpapi.py. The backup key is fetched via the MS-LSAD
LsarRetrievePrivateData RPC call and exported to PVK and PEM files on disk.

## Arguments
- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: Username for authentication (without domain prefix). No default (required).
- **password**: Password for authentication. No default (required).
- **output_dir**: Directory to store the exported backup key files. Defaults to `/tmp/dpapi_backup_key`.

## Requirements
- **Platforms:** Linux, macOS

## Example(s)
```bash
ttpforge run forgearmory//ttps/credential-access/retrieve-dpapi-backup-key/ttp.yaml \
  --arg username=jsmith \
  --arg password='P@ssw0rd'
```

## Steps
1. **setup_impacket**: Set up Python virtual environment with impacket.
2. **retrieve_backup_key**: Retrieve the DPAPI domain backup key from the DC via MS-LSAD RPC and export to PVK and PEM files. Cleanup removes the output directory.
