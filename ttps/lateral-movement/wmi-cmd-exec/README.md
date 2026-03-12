# WMIC Process Call Create

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP (Tactic, Technique, and Procedure) enables the remote execution of
commands on a target system using WMIC (Windows Management Instrumentation
Command-line). It primarily focuses on creating a process on a remote system
to execute a specified command and retrieve the command output.

## Arguments

- **command_or_path**: The command or path of the executable to run on the
  target system.
 
  Default: hostname

- **detect**: Boolean flag to enable detection of remote process creation
  events.

  Default: true

- **target_system**: The hostname or IP address of the target system.

- **remote_cmd_output_file**: The file where the output of the remote command
  will be stored.
 
  Default: cmd_output.txt

## Pre-requisites

1. The executing machine must have network access to the target system.
 
2. Adequate permissions to use WMIC for remote execution on the target system.

3. The target system must be running a compatible version of Windows with
   WMIC and remote management enabled.

## Examples

Run the TTP using the following command (adjust arguments as needed):

```bash
.\ttpforge.exe run forgearmory//lateral-movement/wmi-cmd-exec/ttp.yaml -a target_system=192.168.1.100
```

You can specify a different command or output file:

```bash
.\ttpforge.exe run forgearmory//lateral-movement/wmi-cmd-exec/ttp.yaml -a target_system=192.168.1.100 --a command_or_path="ipconfig /all" --a remote_cmd_output_file="network_info.txt"
```

To run the TTP with detection of remote process creation events:

```bash
ttpforge run forgearmory//lateral-movement/wmi-cmd-exec/ttp.yaml \
  --arg target_system=192.168.1.100 \
  --arg detect=true
```

## Steps

1. **create-remote-process**: Executes the command on the remote system using
   WMIC.

2. **retrieve-output**: Retrieves the output of the remote command from the
   specified output file.

3. **check-detection**: (Optional) Checks for remote process creation events
   in the event log of the executing machine.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0008 Lateral Movement

- **Techniques**:
  - T1021 Remote Services
