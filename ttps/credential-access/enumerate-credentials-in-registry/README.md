# Enumeration for Credentials in Registry

## Description
Searches Windows Registry hives (HKEY_LOCAL_MACHINE and HKEY_CURRENT_USER) for registry keys or values containing "password". Some applications insecurely store credentials in the Registry in plaintext or weakly encrypted formats.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//credential-access/enumerate-credentials-in-registry/ttp.yaml
```

## Steps
1. **enumerate_hklm_passwords**: Queries the HKEY_LOCAL_MACHINE registry hive recursively to find all registry keys containing the word "password" in REG_SZ (string) type values.
2. **enumerate_hkcu_passwords**: Queries the HKEY_CURRENT_USER registry hive recursively to find all registry keys containing the word "password" in REG_SZ (string) type values.
