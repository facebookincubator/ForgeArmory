# Execute Command with Kerberos Ticket

## Description

Executes a command on a remote host using a forged or stolen Kerberos ticket (ccache file)
via NetExec (nxc). Supports multiple protocols including SMB, WinRM, and WMI for flexible
lateral movement.

## Arguments

- **ticket_path**: Path to the Kerberos .ccache ticket file (e.g., /tmp/golden_ticket.ccache). No default.
- **command**: The command to execute on the remote host. No default.
- **target**: The target host to execute the command on (must be a FQDN that matches the ticket's SPN). No default.
- **domain**: The target Active Directory domain. Defaults to `contoso.local`.
- **protocol**: The protocol to use for remote command execution. Choices: `smb`, `winrm`, `wmi`. Defaults to `smb`.
- **dc_ip**: IP address or hostname of the Domain Controller for Kerberos ticket resolution. Defaults to `dc01.contoso.local`.

## Requirements

- Platform: Linux or macOS

## Example(s)

```bash
ttpforge run forgearmory//ttps/lateral-movement/execute-command-with-ticket/ttp.yaml \
  --arg ticket_path=/tmp/golden_ticket.ccache \
  --arg command="whoami" \
  --arg target=server01.contoso.local \
  --arg domain=contoso.local \
  --arg protocol=smb \
  --arg dc_ip=dc01.contoso.local
```

## Steps

1. **setup_netexec**: Set up Python virtual environment with NetExec.
2. **execute_command**: Execute a command on the remote host using the provided Kerberos ticket via NetExec with Kerberos authentication.
