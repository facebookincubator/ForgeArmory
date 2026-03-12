# Forge SSH Certificate with High Priv Principal (Shell)

## Description
Generates an SSH keypair and uses it to create a signed certificate with the high privileged principal `root` directly from the shell (without sudo). This TTP is designed to trigger detection rules for unauthorized SSH certificate generation. It validates that shell-based logging captures the ssh-keygen activity.

## Arguments
This TTP does not take any arguments.

## Requirements
- No special requirements beyond shell access.

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//credential-access/forge-certificate-with-shell/ttp.yaml
```

## Steps
1. **generate_ssh_keypair**: Generates an RSA SSH keypair (`host_key` and `host_key.pub`). Cleanup removes the generated key files.
2. **forge_certificate**: Signs the public key with the high privileged principal `root` using `ssh-keygen`. Cleanup removes the generated certificate file.
