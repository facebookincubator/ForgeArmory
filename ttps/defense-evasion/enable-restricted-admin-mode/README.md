# Enabling Restricted Admin Mode via Command_Prompt

## Description
Enables Restricted Admin Mode for RDP through registry modifications, allowing pass-the-hash attacks using only NTLM hashes. Transforms a security feature into an attack vector for lateral movement across Windows networks without needing plaintext passwords.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **backup_location**: Path where registry backup will be saved (default: `C:\Users\Public\backup.reg`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/enable-restricted-admin-mode/ttp.yaml \
  --backup_location "C:\Temp\lsa_backup.reg"
```

## Steps
1. **backup_registry**: Exports the current LSA (Local Security Authority) registry settings from HKLM\system\currentcontrolset\control\lsa to a backup file for restoration during cleanup.
2. **enable_restricted_admin_mode**: Modifies the DisableRestrictedAdmin registry value in HKLM\system\currentcontrolset\control\lsa, setting it to 0 to enable Restricted Admin Mode for RDP pass-the-hash attacks.
