# SSH ControlMaster Installation

## Description
This TTP appends SSH ControlMaster configuration to the user's `~/.ssh/config` file. SSH ControlMaster allows multiple SSH sessions to share a single network connection, which can be abused by an attacker to hijack existing SSH sessions for lateral movement without re-authenticating.

## Arguments
- **timeout**: Time in seconds before cleanup starts. Default: `120`

## Requirements
- Linux operating system

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//lateral-movement/install-ssh-controlmaster/ttp.yaml --arg timeout=300
```

## Steps
1. **append_to_config**: Back up the existing `~/.ssh/config` file (if present), then append SSH ControlMaster configuration (ControlMaster auto, ControlPath, ControlPersist 10m) to it. Also creates the `~/.ssh/sockets` directory with appropriate permissions. On cleanup, the original config is restored (or the created config is removed) and the sockets directory is deleted.
