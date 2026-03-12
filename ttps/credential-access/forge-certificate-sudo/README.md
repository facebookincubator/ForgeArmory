# Forge SSH Certificate with High Priv Principal (Sudo)

## Description
Generates an SSH keypair and uses it to create a signed certificate with the high privileged principal `root` via sudo. This TTP is designed to trigger detection rules for unauthorized SSH certificate generation via both shell and sudo logging. Sudo logging is built into the sudo binary and sent to syslog, which captures the command line parameters.

## Arguments
This TTP does not take any arguments.

## Requirements
- Sudo access is required to forge the certificate.

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//credential-access/forge-certificate-sudo/ttp.yaml
```

## Steps
1. **generate_ssh_keypair**: Generates an RSA SSH keypair (`host_key` and `host_key.pub`). Cleanup removes the generated key files.
2. **forge_certificate**: Uses `sudo ssh-keygen` to sign the public key with the high privileged principal `root`. Cleanup removes the generated certificate file.
