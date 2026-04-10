# Add GPO Logon Script

## Description

Abuses write access to a Group Policy Object (GPO) to add a logon or startup script.
Scripts are uploaded to SYSVOL and registered in scripts.ini (batch/cmd/vbs) or
psscripts.ini (PowerShell). They execute when users log on or computers start.

## Arguments

- **domain**: The target Active Directory domain (e.g., contoso.com). Defaults to `contoso.local`.
- **dc**: The Domain Controller IP or hostname to target. Defaults to `dc01.contoso.local`.
- **username**: Username for authentication (without domain prefix). No default.
- **password**: Password for authentication. No default.
- **gpo_id**: The GPO GUID to modify (e.g., 12345677-ABCD-9876-ABCD-123456789012). No default.
- **filename**: Filename to create on target (.bat/.cmd/.vbs for batch, .ps1 for PowerShell). Defaults to `logon.bat`.
- **content**: Script content to execute. Defaults to `whoami > C:\Windows\Temp\logon_output.txt`.
- **event**: Script event (Logon/Logoff for users, Startup/Shutdown for machines). Choices: `Logon`, `Logoff`, `Startup`, `Shutdown`. Defaults to `Logon`.

## Requirements

- Platform: Linux or macOS

## Example(s)

```bash
ttpforge run forgearmory//ttps/privilege-escalation/add-gpo-logon-script/ttp.yaml \
  --arg username=admin \
  --arg password=P@ssw0rd \
  --arg gpo_id=12345677-ABCD-9876-ABCD-123456789012 \
  --arg filename=logon.bat \
  --arg content="whoami > C:\Windows\Temp\logon_output.txt" \
  --arg event=Logon
```

## Steps

1. **setup_impacket**: Set up Python virtual environment with impacket and ldap3.
2. **add_logon_script**: Add a logon/startup script to the target GPO via SYSVOL.
3. **Cleanup (add_logon_script)**: Remove the logon/startup script from the GPO by running the script with the `--cleanup` flag.
