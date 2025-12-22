# Staging Local Certificates via Export-Certificate

## Description
Exports all user certificates from CurrentUser\My certificate store and packages them into a compressed archive. These certificates often contain authentication credentials and private keys used for system access.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **archive_path**: Path where the certificate archive will be created (default: `C:\Users\Public\certs.zip`)
- **export_path**: Directory path where certificates will be exported before archiving (default: `C:\Users\Public\certs`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//credential-access/export-user-certificates/ttp.yaml \
  --archive_path "C:\Temp\stolen_certs.zip" \
  --export_path "C:\Temp\cert_export"
```

## Steps
1. **export_and_archive_certificates**: Creates an export directory, iterates through all certificates in the current user's certificate store (Cert:\CurrentUser\My), exports each certificate as a .cer file named with its FriendlyName, and compresses all exported certificates into a ZIP archive.
