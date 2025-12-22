# UAC bypassed by Utilizing ProgIDs registry

## Description
Exploits Windows Registry ProgIDs to bypass UAC by hijacking the ms-settings handler. Creates a malicious file association (.pwn) and redirects execution when auto-elevated binaries like fodhelper.exe are launched. Used by ValleyRAT malware.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/bypass-uac-using-progids/ttp.yaml
```

## Steps
1. **bypass_uac_progids**: Creates registry entries for a custom .pwn file extension with a shell open command pointing to calc.exe, modifies ms-settings\CurVer to redirect to the .pwn handler, and launches fodhelper.exe to trigger the UAC bypass and execute the payload with elevated privileges.
