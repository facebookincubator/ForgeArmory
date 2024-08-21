# Identify Privilege Escalation Paths with Linux Smart Enumeration

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP helps identify privilege escalation paths using Linux Smart
Enumeration, a tool that automates the discovery of local privilege escalation
vulnerabilities on Linux-based operating systems.

## Arguments

- **escalate_privileges**: A boolean flag indicating whether to run the TTP as
  root or not. Default is false.
- **download_link**: The URL to download the latest version of `lse.sh` from
  GitHub. Default is
  [https://github.com/diego-treitos/linux-smart-enumeration/releases/latest/download/lse.sh](https://github.com/diego-treitos/linux-smart-enumeration/releases/latest/download/lse.sh)

## Pre-requisites

1. A Linux-based operating system.
2. Bash shell.

## Examples

You can run the TTP using the following example (after updating the arguments):

```bash
ttpforge run forgearmory//privilege-escalation/linux/identify-privilege-escalation-paths-with-lse/identify-privilege-escalation-paths-with-lse.yaml \
  --arg escalate_privileges=true
```

## Steps

1. **ensure-root-user-if-required**: This step checks if the TTP needs to be run
   as root and ensures that it is being executed as the root user.
2. **download-and-run-lse**: This step downloads the latest version of `lse.sh`
   from GitHub and executes it with bash.

## Manual Reproduction Steps

```
# Escalate privileges to root (optional - being root gives you more info)
sudo su

# Download and run lse
curl -sL https://github.com/diego-treitos/linux-smart-enumeration/releases/latest/download/lse.sh | bash
```

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Execution
  - TA0007 Discovery
- **Techniques**:
  - T1059 Command and Scripting Interpreter
  - T1087 Account Discovery
  - T1083 File and Directory Discovery
  - T1057 Process Discovery
  - T1069 Permission Groups Discovery
  - T1518 Software Discovery
  - T1082 System Information Discovery
  - T1033 System Owner/User Discovery
  - T1007 System Service Discovery
- **Subtechniques**:
  - T1059.004 Command and Scripting Interpreter Unix Shell
