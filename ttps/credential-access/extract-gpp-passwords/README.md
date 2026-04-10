# Extract Passwords from Group Policy Preferences

## Description
Enumerates and extracts plaintext passwords from Group Policy Preferences (GPP) XML files on SYSVOL.

This TTP performs the following:
1. Enumerates all XML files on SYSVOL (equivalent to: dir /s *.xml)
2. Downloads only GPP-related XML files (Groups.xml, Services.xml, etc.)
3. Extracts and decrypts cpassword values using the known AES key (MS14-025)

## Arguments
- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: Username in DOMAIN\\user format for SMB authentication. No default (required).
- **password**: Password for SMB authentication. No default (required).
- **output_dir**: Local directory to save downloaded files. Defaults to `/tmp/gpp_extraction`.

## Requirements
- **Platforms:** Linux

## Example(s)
```bash
ttpforge run forgearmory//ttps/credential-access/extract-gpp-passwords/ttp.yaml \
  --arg username='CONTOSO\jsmith' \
  --arg password='P@ssw0rd'
```

## Steps
1. **download_gpp_xml_files**: Download GPP XML files from SYSVOL. Retrieves Groups.xml, Services.xml, ScheduledTasks.xml, DataSources.xml, Printers.xml, and Drives.xml.
2. **extract_gpp_passwords**: Extract and decrypt cpassword values from downloaded XML files using the publicly known Microsoft AES key (MS14-025). Cleanup removes the output directory.
