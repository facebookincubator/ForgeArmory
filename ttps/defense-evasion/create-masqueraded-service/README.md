# Creating W32Time similar named service using sc

## Description
Creates Windows services with names similar to legitimate system services (e.g., "win32times" mimicking "W32Time") to evade detection. Used by "Operation Wocao" threat actor group. Provides persistence and execution capabilities while blending in with legitimate services.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **command**: Command to execute (default: `powershell.exe -c whoami`)
- **service_name**: Name of the service to create (default: `win32times`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/create-masqueraded-service/ttp.yaml \
  --command "powershell.exe -c calc.exe" \
  --service_name "win32service"
```

## Steps
1. **create_masqueraded_service**: Creates a Windows service with a masqueraded name using sc.exe, configures it to execute the specified command, and queries the service configuration to verify creation.
