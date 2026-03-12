# Disable Event Logging in Windows

## Description
This TTP disables Windows Event Logging by stopping the Windows Event Log service. This technique can be used by adversaries to hide malicious activity from security tools that rely on Windows event logs for detection. This simulates a defense evasion technique documented in DFIR reports related to Exchange exploits leading to domain-wide ransomware.

## Arguments
This TTP takes no arguments.

## Requirements
- Platform: Windows
- PowerShell
- Superuser (Administrator) privileges are required

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/disable-event-logging/ttp.yaml
```

## Steps
1. **Disable event logging and delete logs**: Stops the Windows Event Log service using `net stop eventlog /y` and verifies the service is stopped using `Get-Service eventlog`. The cleanup step re-enables event logging by starting the service again and verifying it is running.
