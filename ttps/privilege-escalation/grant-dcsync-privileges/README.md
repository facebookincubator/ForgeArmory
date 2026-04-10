# Grant DCSync Privileges via DACL Modification

## Description

Grants DCSync replication privileges (DS-Replication-Get-Changes and
DS-Replication-Get-Changes-All) to a target principal by modifying the DACL
on the domain root object. Uses Impacket's dacledit.py with the -rights DCSync flag.
A backup of the original DACL is saved to a user-specified directory (default: /tmp),
and cleanup restores the DACL from that backup.

## Arguments

- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: Username for authentication (without domain prefix). No default.
- **password**: Password for authentication. No default.
- **target_principal**: The sAMAccountName of the principal to grant DCSync privileges to. No default.
- **backup_path**: Path to store the DACL backup file created by dacledit. Defaults to `/tmp/dacledit.bak`.

## Requirements

- Platform: Linux or macOS

## Example(s)

```bash
ttpforge run forgearmory//ttps/privilege-escalation/grant-dcsync-privileges/ttp.yaml \
  --arg username=admin \
  --arg password=P@ssw0rd \
  --arg target_principal=jdoe \
  --arg domain=contoso.local \
  --arg dc=dc01.contoso.local
```

## Steps

1. **setup_impacket**: Set up Python virtual environment with impacket.
2. **grant_dcsync**: Grant DCSync replication privileges to the target principal by writing an ACE to the domain root DACL.
3. **Cleanup (grant_dcsync)**: Restore the original DACL from the backup file and remove backup files.
