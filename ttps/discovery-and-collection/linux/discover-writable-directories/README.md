# Discover Writable Directories

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP discovers writable directories in the specified directory.

## Arguments

- **seed_dir**: The starting directory to search for writable directories. Defaults to '.' if not provided.

## Prerequisites

1. The executor must have read access to the specified directory and its subdirectories.

## Examples

You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//discovery/linux/discover-writable-directories/discover-writable-directories.yaml \
  --arg seed_dir=/path/to/directory
```

## Steps

1. find-writable-directories: This step uses the find command to discover writable directories in the specified directory.

## Manual Reproduction Steps

```
# Escalate privileges to root
# (optional - being root gives you more info)
sudo su

SEED_DIR='.'

# Discover writable directories
find "${SEED_DIR}" -writable
```

## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0007 Discovery
- **Techniques**:
    - T1083 File and Directory Discovery
