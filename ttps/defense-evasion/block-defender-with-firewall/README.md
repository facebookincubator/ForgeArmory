# Block Microsoft Defender with Firewall

## Description
Blocks Windows Defender (MsMpEng.exe) network communications via firewall rules. Prevents signature updates, cloud analysis, and telemetry, allowing malware to operate with reduced risk of detection.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **rule_name**: Name of the firewall rule (default: `Atomic Test`)
- **exe_file_path**: Path to exe file (default: `C:\ProgramData\Microsoft\Windows Defender\Platform\4.18.25080.5-0\MsMpEng.exe`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/block-defender-with-firewall/ttp.yaml \
  --rule_name "Custom Block Rule" \
  --exe_file_path "C:\ProgramData\Microsoft\Windows Defender\Platform\4.18.25080.5-0\MsMpEng.exe"
```

## Steps
1. **ensure_exe_exists**: Verifies that the Windows Defender executable exists at the specified path before attempting to create the firewall rule. If the executable is not found, the test exits with an error.
2. **block_exe_with_firewall**: Uses netsh advfirewall to add an outbound blocking firewall rule for the Windows Defender executable.
