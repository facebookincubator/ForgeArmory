# Discover SUID/SGID Binaries

## Description
This TTP searches for any binaries with the SUID or SGID bits set. Discovering SUID/SGID binaries is a common reconnaissance technique used to identify potential vectors for privilege escalation.

## Arguments
This TTP takes no arguments.

## Requirements
- Linux operating system

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//discovery/discover-suid-sgid-binaries/ttp.yaml
```

## Steps
1. **suid_search**: Run two find commands to search for binaries with the SUID bit (`-perm -4000`) and SGID bit (`-perm -2000`) set in the current directory. No cleanup is needed as this step only runs shell commands.
