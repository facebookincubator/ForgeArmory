# Add Root Certificate to CurrentUser Certificate Store

## Description
Installs a malicious root certificate into the CurrentUser certificate store. Enables man-in-the-middle attacks, traffic decryption, and bypassing SSL/TLS warnings. Allows attackers to sign code, impersonate websites, or decrypt HTTPS traffic without triggering security warnings.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **script_path**: Path to RemoteCertTrust.ps1 script (default: `./RemoteCertTrust.ps1`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/install-root-ca-certstore/ttp.yaml \
  --script_path "C:\Scripts\RemoteCertTrust.ps1"
```

## Steps
1. **ensure_script_exists**: Verifies that the RemoteCertTrust.ps1 script exists at the specified path before attempting execution. If the script is not found, the test exits with an error.
2. **add_certificate_to_currentuser_store**: Sources and executes the RemoteCertTrust.ps1 script to add a generic certificate to the CurrentUser certificate store, which generates registry modifications adding the certificate.
