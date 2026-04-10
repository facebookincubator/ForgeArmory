# Create Computer Account

## Description
Creates a computer account in Active Directory using Impacket's addcomputer.py.
Outputs the computer name for use by subsequent steps or parent TTPs.
Cleanup deletes the created computer account.

## Arguments
- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: Username for authentication (without domain prefix). No default (required).
- **password**: Password for authentication. No default (required).
- **computer_name**: Name for the new computer account (without trailing $). No default (required).
- **computer_password**: Password to set on the computer account. Defaults to `P@ssw0rd123!`.
- **method**: Method to use for account creation (LDAPS or SAMR). LDAPS creates object directly via LDAPS. SAMR uses SamrCreateUser2InDomain. Defaults to `LDAPS`.

## Requirements
- **Platforms:** Linux, macOS

## Example(s)
```bash
ttpforge run forgearmory//ttps/utils/create-computer-account/ttp.yaml \
  --arg username=jsmith \
  --arg password='P@ssw0rd' \
  --arg computer_name=YOURPC01
```

## Steps
1. **setup_impacket**: Set up Python virtual environment with impacket.
2. **create_computer**: Create a computer account via addcomputer.py. Cleanup deletes the created computer account.
