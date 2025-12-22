# Enable RDP Multi-Session Features

## Description
Enables multiple RDP and remote session capabilities (multiple RDP sessions per user, multiple user sessions, RDP shadowing, Windows Remote Assistance) through registry modifications and firewall changes. Observed in Mimic ransomware and Azorult. Establishes covert remote access channels bypassing normal controls.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **server_name**: The remote server that we need to shadow and have to do the registry modification (default: `localhost`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/enable-rdp-multi-session-features/ttp.yaml \
  --server_name "TARGET-PC"
```

## Steps
1. **allow_multiple_rdp_sessions**: Modifies the fSingleSessionPerUser registry value in HKLM\System\CurrentControlSet\Control\Terminal Server, setting it to 0 to allow multiple RDP sessions per user.
2. **enable_multiple_sessions**: Sets AllowMultipleTSSessions to 1 in HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Winlogon registry key, enabling multiple Terminal Services sessions for the current user.
3. **enable_rdp_shadowing**: Creates a CIM session to the specified server, enables the "Remote Desktop - Shadow (TCP-In)" firewall rule, and sets the shadow registry value to 2 in the Terminal Services registry key to enable full control shadowing.
4. **allow_rdp_remote_assistance**: Sets fAllowToGetHelp to 1 in HKLM\System\CurrentControlSet\Control\Terminal Server registry key, enabling Windows Remote Assistance connections.
