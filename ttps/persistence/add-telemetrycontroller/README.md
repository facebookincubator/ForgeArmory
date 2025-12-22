# Abusing Windows TelemetryController Registry Key for Persistence

## Description
Abuses Windows Compatibility Telemetry (CompatTelRunner.exe) by injecting malicious commands into TelemetryController registry keys. Executes arbitrary commands with SYSTEM privileges. Stealthy persistence technique that blends with legitimate telemetry operations.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **new_key**: New Registry Key Added (default: `NewKey`)
- **executable_path**: Custom Executable to run (default: `C:\Windows\System32\cmd.exe`)
- **backup_location**: Path where registry backup will be saved (default: `C:\Users\Public\backup.reg`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//persistence/add-telemetrycontroller/ttp.yaml \
  --new_key "MaliciousTelemetry" \
  --executable_path "C:\Malware\backdoor.exe"
```

## Steps
1. **backup_registry**: Exports the current TelemetryController registry settings to a backup file for restoration during cleanup.
2. **add_telemetry_controller_key**: Creates a new registry key under TelemetryController with the specified name and sets a Command value (REG_SZ) pointing to the custom executable, establishing persistence through the Windows Compatibility Telemetry system.
