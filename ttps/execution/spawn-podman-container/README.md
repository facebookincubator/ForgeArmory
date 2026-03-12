# Spawn Podman Container

## Description
This TTP tests the CGroups detection for rogue containers on compute hosts. It checks if podman is installed (installs it if not present), loads an Ubuntu 20.04 container image from a bundled image.tar file, and then executes into the container.

## Arguments
- **timeout**: Timeout value to set before cleanup begins. Default: `900`

## Requirements
- Linux operating system

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/spawn-podman-container/ttp.yaml --arg timeout=600
```

## Steps
1. **exec_container**: Install podman and expect packages if not present, load the Ubuntu 20.04 container image from image.tar, spawn the container using the bundled spawn-podman.sh script, and sleep for the timeout duration. On cleanup, all running podman containers are killed and the podman and expect packages are removed.
