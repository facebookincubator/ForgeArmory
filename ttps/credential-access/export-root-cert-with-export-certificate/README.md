# Export Root Certificate with Export-Certificate

## Description
Creates a self-signed root certificate and exports it using Export-Certificate cmdlet. Self-signed certificates can be used to sign malicious code, establish encrypted communications, or impersonate certificate authorities.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **pfx_path**: Path of the certificate (default: `C:\Users\Public\AtomicRedTeam.cer`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//credential-access/export-root-cert-with-export-certificate/ttp.yaml \
  --pfx_path "C:\Temp\mycert.cer"
```

## Steps
1. **create_and_export_certificate**: Creates a new self-signed certificate for atomicredteam.com in the LocalMachine\My certificate store, then exports it to the specified file path using Export-Certificate.
