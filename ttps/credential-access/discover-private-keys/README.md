# Private Keys

## Description
Searches for private key files with common extensions (.key, .pgp, .gpg, .ppk, .p12, .pem, .pfx, .cer, .p7b, .asc) on the Windows file system. Access to these cryptographic files can enable decryption, authentication, and unauthorized system access.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//credential-access/discover-private-keys/ttp.yaml
```

## Steps
1. **search_for_private_keys**: Recursively searches the C:\ drive for files with the .key extension using the dir and findstr commands to locate potential private key files on the system.
