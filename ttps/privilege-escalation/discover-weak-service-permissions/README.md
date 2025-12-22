# Service Registry Permissions Weakness

## Description
Discovers weak service registry permissions that can lead to privilege escalation. Enumerates ACLs on service registry keys using Get-Acl. If misconfigured, attackers can modify ImagePath to point to malicious executables that run with SYSTEM-level privileges when service restarts.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **weak_service_name**: Service to check for weak permissions (default: `weakservicename`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//privilege-escalation/discover-weak-service-permissions/ttp.yaml
```

## Steps
1. **check_service_registry_permissions**: Uses the Get-Acl PowerShell cmdlet to retrieve Access Control Lists (ACLs) for the first 10 service registry keys under HKLM\SYSTEM\CurrentControlSet\Services\, displaying detailed permission information that can reveal weak permissions exploitable for privilege escalation.
