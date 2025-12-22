# Modifying ACL of Service Control Manager via SDSET

## Description
Demonstrates privilege escalation by modifying the Service Control Manager (SCM) ACL to grant SYSTEM-level access. Uses `sc.exe sdset` to modify the SCM security descriptor, granting full control to all users. Administrative users can then create services with SYSTEM privileges, bypassing UAC. A system restart may be required. Used by attackers escalating from administrative to SYSTEM privileges. Reference: https://0xv1n.github.io/posts/scmanager/

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **backup_file_path**: Path where the original SCM ACL will be backed up (default: `C:\Users\Public\scmanager_acl_backup.txt`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP
2. System restart may be required for changes to take full effect

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/modify-acl-of-scm/ttp.yaml \
  --backup_file_path "C:\Temp\scm_backup.txt"
```

## Steps
1. **backup_scmanager_acl**: Uses sc.exe with the sdshow command to retrieve and save the current Service Control Manager security descriptor to a backup file for restoration during cleanup.
2. **modify_scmanager_acl**: Uses sc.exe with the sdset command to modify the SCM security descriptor, granting full control (KA) to all users (WD), which allows any administrative user to create and manage services with SYSTEM privileges.
