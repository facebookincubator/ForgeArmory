# Export Root Certificate with Export-PFXCertificate

## Description
Creates a self-signed root certificate and exports it as a password-protected PFX file using Export-PFXCertificate. PFX files contain both the certificate and private key, enabling certificate impersonation and man-in-the-middle attacks.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **pfx_path**: output path of the certificate (default: `C:\Users\Public\atomicredteam.pfx`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//credential-access/export-root-cert-with-export-pfxcertificate/ttp.yaml \
  --pfx_path "C:\Temp\exported.pfx"
```

## Steps
1. **create_and_export_certificate**: Creates a secure password string "AtomicRedTeam", generates a new self-signed certificate for atomicredteam.com in the LocalMachine\My certificate store, and exports it as a password-protected PFX file using Export-PfxCertificate.
