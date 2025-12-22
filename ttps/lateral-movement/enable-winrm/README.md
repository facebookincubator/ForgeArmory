# Enable Windows Remote Management

## Description
Enables WinRM and PowerShell Remoting to facilitate lateral movement and remote command execution. Establishes persistent remote access capabilities that blend with normal IT operations. Starts WinRM service, creates firewall exceptions, and registers PowerShell session configurations. Observed in numerous APT campaigns.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//lateral-movement/enable-winrm/ttp.yaml
```

## Steps
1. **enable_psremoting**: Executes the Enable-PSRemoting cmdlet with the -Force parameter to enable PowerShell Remoting and configure WinRM without prompting for user confirmation.
