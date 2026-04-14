# SMB File Download

## Description
Generic utility to download files from an SMB share.

This TTP connects to an SMB share and downloads files from a specified
remote path to a local directory.

## Arguments
- **server**: The SMB server hostname or IP address. No default (required).
- **share**: The SMB share name (e.g., SYSVOL, C$, NETLOGON). No default (required).
- **remote_path**: The path on the remote share to download from (e.g., "domain.com/Policies/{GUID}"). No default (required).
- **username**: The username in DOMAIN\\user format for SMB authentication. No default (required).
- **password**: The password for the user. No default (required).
- **output_dir**: Local directory to save downloaded files. Defaults to `/tmp/smb_download`.
- **recurse**: Whether to recursively download files. Defaults to `true`.
- **ignore_errors**: Whether to ignore errors and continue downloading files. Defaults to `false`.

## Requirements
- **Platforms:** Linux

## Example(s)
```bash
ttpforge run forgearmory//ttps/utils/smb-download/ttp.yaml \
  --arg server=dc01.contoso.local \
  --arg share=SYSVOL \
  --arg remote_path='contoso.local/Policies' \
  --arg username='CONTOSO\jsmith' \
  --arg password='P@ssw0rd'
```

## Steps
1. **ensure_smbclient_installed**: Install smbclient if not already installed.
2. **download_from_smb**: Connect to SMB share and download files. Supports recursive downloads. Cleanup removes the output directory.
