# Modify AdminSDHolder DACL

## Description

Reads and then modifies the DACL on the AdminSDHolder container. First reads
the current DACL for visibility, then grants a target principal full control
(GenericAll) over all protected Active Directory accounts and groups.

## Arguments

- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: Username for authentication (without domain prefix). No default.
- **password**: Password for authentication. No default.
- **target_principal**: The sAMAccountName of the principal to grant GenericAll on AdminSDHolder. No default.
- **backup_path**: Path to store the DACL backup file created by dacledit. Defaults to `/tmp/adminsdholder_dacledit.bak`.

## Requirements

- Platform: Linux or macOS

## Example(s)

```bash
ttpforge run forgearmory//ttps/privilege-escalation/modify-adminsdholder-dacl/ttp.yaml \
  --arg username=admin \
  --arg password=P@ssw0rd \
  --arg target_principal=jdoe \
  --arg domain=contoso.local \
  --arg dc=dc01.contoso.local
```

## Steps

1. **setup_impacket**: Set up Python virtual environment with impacket.
2. **read_adminsdholder_dacl**: Read the current DACL on the AdminSDHolder container for visibility.
3. **write_adminsdholder_dacl**: Grant GenericAll to the target principal on the AdminSDHolder container.
4. **Cleanup (write_adminsdholder_dacl)**: Restore the original DACL on AdminSDHolder from the backup file and remove backup files.
