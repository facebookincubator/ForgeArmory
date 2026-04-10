# Link GPO and Abuse with Scheduled Task

## Description

This chain TTP performs an end-to-end GPO abuse attack by first linking a GPO to
a target OU, then adding a malicious scheduled task to the GPO.

The attack chain:
1. Link the GPO to a target OU using pyGPO
2. Add a scheduled task to the GPO using a custom Impacket-based script

## Arguments

- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: Username for authentication (without domain prefix). No default.
- **password**: Password for authentication. No default.
- **gpo_id**: The GPO GUID to link and abuse (e.g., 12345677-ABCD-9876-ABCD-123456789012). No default.
- **target_dn**: The distinguished name of the OU to link the GPO to (e.g., OU=Workstations,DC=contoso,DC=com). No default.
- **command**: Command to execute via the scheduled task. Defaults to `whoami`.
- **taskname**: Name of the scheduled task to create. Defaults to `GPOAbuseTask`.

## Requirements

- Platform: Linux or macOS

## Example(s)

```bash
ttpforge run forgearmory//ttps/chains/gpo-link-and-abuse/ttp.yaml \
  --arg username=admin \
  --arg password=P@ssw0rd \
  --arg gpo_id=12345677-ABCD-9876-ABCD-123456789012 \
  --arg target_dn="OU=Workstations,DC=contoso,DC=local" \
  --arg command="whoami" \
  --arg taskname=GPOAbuseTask
```

## Steps

1. **link_gpo**: Link the GPO to the target OU using pyGPO.
2. **abuse_gpo**: Add a scheduled task to the GPO with the specified command.
