# Modify Service to Run Arbitrary Binary (Powershell)

## Description
Modifies Windows service binary paths to execute arbitrary binaries with SYSTEM-level privileges. Temporarily modifies target service (default: Print Spooler) to run malicious payloads. When service restarts, malicious binary executes with elevated privileges. Widely observed in ransomware and APT campaigns.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **service_name**: Name of the service to modify (default: `spooler`)
- **new_bin_path**: Path of the new service binary (default: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`)
- **original_bin_path**: Path of the original service binary (default: `C:\Windows\System32\spoolsv.exe`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//privilege-escalation/modify-service-binary/ttp.yaml \
  --service_name "wuauserv" \
  --new_bin_path "C:\Malware\backdoor.exe" \
  --original_bin_path "C:\Windows\System32\wuaueng.dll"
```

## Steps
1. **modify_and_start_service**: Stops the specified service, uses sc.exe to modify the service's binary path to point to the new executable, then attempts to start the service with the modified configuration.
