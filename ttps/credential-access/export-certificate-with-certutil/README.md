# CertUtil ExportPFX

## Description
Adds a certificate to the Root certificate store and exports it as a PFX file using CertUtil. Mimics techniques observed in Golden SAML attacks where adversaries extract private keys for certificate cloning, code signing abuse, or authentication bypass.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **cert_script_path**: Path to RemoteCertTrust.ps1 script (default: `./RemoteCertTrust.ps1`)
- **output**: file path to export to (default: `C:\Windows\Temp\atomic.pfx`)
- **password**: password for cert (default: `password`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//credential-access/export-certificate-with-certutil/ttp.yaml \
  --cert_script_path "C:\Scripts\RemoteCertTrust.ps1" \
  --output "C:\Temp\exported.pfx"
```

## Steps
1. **ensure_cert_script_exists**: Verifies that the RemoteCertTrust.ps1 script exists at the specified path before attempting execution. If the script is not found, the test exits with an error.
2. **export_certificate_with_certutil**: Sources the RemoteCertTrust.ps1 script and uses certutil.exe with the -exportPFX parameter to export a certificate with a specific thumbprint (1F3D38F280635F275BE92B87CF83E40E40458400) from the Root certificate store to a PFX file.
