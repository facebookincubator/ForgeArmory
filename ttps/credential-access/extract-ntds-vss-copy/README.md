# Extract NTDS.dit from VSS Copy

## Description
Extracts credentials from a Domain Controller by dumping the NTDS.dit database
via a Volume Shadow Copy (VSS). Uses Impacket's secretsdump.py with the -use-vss
flag to create a shadow copy of the system drive, copy the NTDS.dit and SYSTEM
hive, and extract password hashes offline.

## Arguments
- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: Username for authentication (without domain prefix). No default (required).
- **password**: Password for authentication. No default (required).
- **method**: Execution method (smbexec, wmiexec, or mmcexec). Defaults to `smbexec`.

## Requirements
- **Platforms:** Linux, macOS

## Example(s)
```bash
ttpforge run forgearmory//ttps/credential-access/extract-ntds-vss-copy/ttp.yaml \
  --arg username=jsmith \
  --arg password='P@ssw0rd'
```

```bash
ttpforge run forgearmory//ttps/credential-access/extract-ntds-vss-copy/ttp.yaml \
  --arg username=jsmith \
  --arg password='P@ssw0rd' \
  --arg method=wmiexec
```

## Steps
1. **setup_impacket**: Set up Python virtual environment with impacket.
2. **dump_ntds**: Perform NTDS.dit dump via VSS copy using the specified execution method.
