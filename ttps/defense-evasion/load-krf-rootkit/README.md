# Run KRF Rootkit

## Description
This TTP includes a .zip file which contains the KRF Linux kernel module rootkit. It extracts the .zip, runs make, make install, and make insmod to insert the rootkit. The TTP also verifies that the krfx kernel module has been successfully inserted.

## Arguments
- **timeout**: Timeout value to set before cleanup begins. Default: `120`

## Requirements
- Linux operating system
- Superuser (root) privileges

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/load-krf-rootkit/ttp.yaml --arg timeout=300
```

## Steps
1. **build_kernelmodule**: Install required dependencies (kernel-devel, Development Tools, ruby, elfutils-libelf-devel), extract krf.zip, build the kernel module, install it, and insert it using insmod. On cleanup, the TTP sleeps for the specified timeout, removes installed packages, removes the krfx kernel module, and deletes the extracted files.
