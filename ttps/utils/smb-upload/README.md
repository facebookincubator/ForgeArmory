# SMB File Upload

## Description
Generic utility to upload a local file to an SMB share.

This TTP connects to an SMB share and uploads a local file to a specified
remote path. Creates parent directories as needed.

## Arguments
- **server**: The SMB server hostname or IP address. No default (required).
- **share**: The SMB share name (e.g., SYSVOL, C$, NETLOGON). No default (required).
- **remote_path**: The path on the remote share to upload to (e.g., "domain.com/Policies/{GUID}/Scripts/Logon"). No default (required).
- **local_file**: Local file path to upload. No default (required).
- **username**: The username in DOMAIN\\user format for SMB authentication. No default (required).
- **password**: The password for the user. No default (required).
- **create_dirs**: Whether to create parent directories on the remote share. Defaults to `true`.
- **ignore_errors**: Whether to ignore errors and continue. Defaults to `false`.

## Requirements
- **Platforms:** Linux

## Example(s)
```bash
ttpforge run forgearmory//ttps/utils/smb-upload/ttp.yaml \
  --arg server=dc01.contoso.local \
  --arg share=SYSVOL \
  --arg remote_path='contoso.local/Policies/{GUID}/Scripts/Logon' \
  --arg local_file=/tmp/payload.ps1 \
  --arg username='CONTOSO\jsmith' \
  --arg password='P@ssw0rd'
```

## Steps
1. **ensure_smbclient_installed**: Install smbclient if not already installed.
2. **upload_to_smb**: Connect to SMB share and upload file. Optionally creates parent directories on the remote share. Cleanup removes the uploaded file from the remote share.
