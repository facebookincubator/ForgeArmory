# SSH RC Persistence

## Description
This TTP creates a `~/.ssh/rc` file (if one does not exist) or appends to the rc file (if it exists). When triggered, the rc file will drop a file at `/tmp/testfile`. The `~/.ssh/rc` file is executed each time an inbound SSH session is established, making it a persistence mechanism for maintaining access.

## Arguments
- **timeout**: Timeout value to set before cleanup begins. Default: `900`

## Requirements
- Linux operating system

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//persistence/sshrc-persistence/ttp.yaml --arg timeout=600
```

## Steps
1. **sshrc**: Back up any existing `~/.ssh/rc` file, then create or append a command that writes to `/tmp/testfile`. After sleeping for the specified timeout, the original `~/.ssh/rc` file is restored (or removed if it was newly created) and `/tmp/testfile` is deleted.
