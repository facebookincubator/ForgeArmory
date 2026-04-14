# Link GPO to Organizational Unit

## Description

Links a Group Policy Object (GPO) to an Organizational Unit (OU) using pyGPO.
This is often a prerequisite for GPO abuse - a GPO must be linked to targets
before scheduled tasks or other malicious configurations will apply.

## Arguments

- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: Username for authentication (without domain prefix). No default.
- **password**: Password for authentication. No default.
- **gpo_id**: The GPO GUID to link (e.g., 12345677-ABCD-9876-ABCD-123456789012). No default.
- **target_dn**: The distinguished name of the OU to link the GPO to (e.g., OU=Workstations,DC=contoso,DC=com). No default.

## Requirements

- Platform: Linux or macOS

## Example(s)

```bash
ttpforge run forgearmory//ttps/privilege-escalation/link-gpo/ttp.yaml \
  --arg username=admin \
  --arg password=P@ssw0rd \
  --arg gpo_id=12345677-ABCD-9876-ABCD-123456789012 \
  --arg target_dn="OU=Workstations,DC=contoso,DC=local"
```

## Steps

1. **setup_pygpo**: Set up Python virtual environment with pyGPO.
2. **link_gpo**: Link the GPO to the target OU using pyGPO.
3. **Cleanup (link_gpo)**: Unlink the GPO from the target OU.
