# Download GPO Configuration from SYSVOL

## Description
This TTP downloads Group Policy Object (GPO) configurations from SYSVOL via SMB.

GPO configurations are stored in SYSVOL at:
\\<DOMAIN>\SYSVOL\<DOMAIN>\Policies\{GPO-GUID}\

This TTP uses the smb-download utility for the actual file retrieval.
It accepts a comma-separated list of GPO GUIDs and downloads each one.

## Arguments
- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: The username in DOMAIN\user format for SMB authentication. Defaults to `CONTOSO\admin`.
- **password**: The password for the user. No default (required).
- **gpo_guids**: Comma-separated list of GPO GUIDs to download (e.g., "{GUID1},{GUID2}"). No default (required).
- **output_dir**: Directory to save downloaded GPO configurations. Defaults to `/tmp/gpo_configs`.

## Requirements
- Platform: Linux

## Example(s)
```bash
ttpforge run forgearmory//ttps/discovery/download-gpos-from-sysvol/ttp.yaml \
    --arg domain=contoso.local \
    --arg dc=dc01.contoso.local \
    --arg username='CONTOSO\admin' \
    --arg password=P@ssw0rd \
    --arg gpo_guids='{31B2F340-016D-11D2-945F-00C04FB984F9},{6AC1786C-016F-11D2-945F-00C04fB984F9}'
```

## Steps
1. **prepare_output_directory**: Create base output directory for storing downloaded GPO configurations.
2. **download_gpo_\<GUID\>**: Download each specified GPO from SYSVOL via SMB (one step per GPO GUID).
