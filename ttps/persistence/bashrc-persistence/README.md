# Persistence via .bashrc File

## Description
This TTP creates a `~/.bashrc` file (if one does not exist) or appends to the `.bashrc` file (if it exists). When executed, the modified `.bashrc` file will drop a file at `/tmp/bashrcfiletest`. This simulates an attacker establishing persistence by modifying shell initialization files that are sourced when a bash session is created.

## Arguments
- **timeout**: Timeout value to set before cleanup begins. Default: `900`

## Requirements
- Linux operating system

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//persistence/bashrc-persistence/ttp.yaml --arg timeout=600
```

## Steps
1. **bashrc**: Back up the existing `~/.bashrc` file (creating one if it does not exist), append a command that writes to `/tmp/bashrcfiletest`, source the modified file, and sleep for the specified timeout. On cleanup, the original `.bashrc` file is restored and the dropped `/tmp/bashrcfiletest` file is removed.
