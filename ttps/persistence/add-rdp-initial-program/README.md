# Modify RDP-Tcp Initial Program Registry Entry

## Description
Establishes persistence by auto-launching executables on RDP connection. Modifies fInheritInitialProgram and InitialProgram registry values. Malicious code launches within RDP session context, appearing as legitimate remote desktop activity. Observed in APT campaigns and ransomware operations.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **executable_path**: Custom Executable to run (default: `C:\Windows\System32\cmd.exe`)
- **backup_location**: Path where registry backup will be saved (default: `C:\Users\Public\backup.reg`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//persistence/add-rdp-initial-program/ttp.yaml \
  --executable_path "C:\Malware\backdoor.exe"
```

## Steps
1. **backup_registry**: Exports the current RDP-Tcp registry settings to a backup file for restoration during cleanup.
2. **modify_rdp_initial_program**: Modifies two registry values: sets fInheritInitialProgram to 1 (DWORD) to enable automatic program execution on RDP connection, and sets InitialProgram to the specified executable path, establishing persistence through automatic execution on RDP sessions.
