# Service ImagePath Change with reg.exe

## Description
Exploits weak service registry permissions to modify ImagePath value, achieving privilege escalation. Uses reg.exe to directly modify service registry instead of Service Control Manager API, potentially evading detection. Services run with SYSTEM-level privileges, giving attackers elevated access.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **weak_service_name**: Service with weak permissions (default: `spooler`)
- **weak_service_path**: Original executable path for weak service (default: `C:\Windows\system32\spoolsv.exe`)
- **malicious_service_path**: New executable path to update weak service (default: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`)
- **backup_file_path**: Path where service registry backup will be stored (default: `C:\Users\Public\service_backup.reg`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//privilege-escalation/modify-service-imagepath/ttp.yaml \
  --weak_service_name "vulnerableservice" \
  --malicious_service_path "C:\Malware\backdoor.exe"
```

## Steps
1. **backup_service_registry**: Uses reg.exe to export the entire service registry configuration to a backup file for restoration during cleanup.
2. **modify_service_imagepath**: Uses reg.exe to modify the ImagePath registry value of the specified service, changing it from the legitimate service binary to the malicious executable path, establishing privilege escalation through service hijacking.
