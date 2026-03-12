# Persistence via .bashenv File

## Description
This TTP creates a `~/.bashenv` file (if one does not exist) or appends to the `.bashenv` file (if it exists). When executed, the modified `.bashenv` file will drop a file at `/tmp/bashenvout`. This simulates an attacker establishing persistence by modifying shell environment files that are sourced when a bash session is created.

## Arguments
- **timeout**: Timeout value to set before cleanup begins. Default: `900`

## Requirements
- Linux operating system

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//persistence/bashenv-persistence/ttp.yaml --arg timeout=600
```

## Steps
1. **bashenv**: Back up the existing `~/.bashenv` file (creating one if it does not exist), append a command that writes to `/tmp/bashenvout`, source the modified file, and sleep for the specified timeout. On cleanup, the original `.bashenv` file is restored and the dropped `/tmp/bashenvout` file is removed.
