# Install root CA on Windows

## Description
Creates and installs a malicious root CA certificate on Windows. Enables man-in-the-middle attacks, SSL/TLS traffic decryption, code signing with trusted certificates, and bypassing security warnings by establishing system-wide trust for self-signed certificates.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **pfx_path**: Path of the certificate (default: `C:\Users\Public\rootCA.cer`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/install-root-ca-certutil/ttp.yaml \
  --pfx_path "C:\Certificates\malicious-ca.cer"
```

## Steps
1. **ensure_certificate_exists**: Checks if the certificate file already exists at the specified path. If not, creates a new self-signed certificate for atomicredteam.com in the LocalMachine\My certificate store and exports it as a CER file to the specified path.
2. **install_root_ca**: Imports the certificate from the file into the LocalMachine\My certificate store, then moves it to the LocalMachine\Root certificate store to establish it as a trusted root CA for system-wide trust.
