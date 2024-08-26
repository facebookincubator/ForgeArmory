# Discover Installed Software on MacOS

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP discovers software installed on a MacOS machine.

## Arguments
- **brew**:  a boolean flag specifying enumeration of software installed using brew
- **mdfind**: a boolean flag specifying enumeration of software installed using mdfind
- **sp**: a boolean flag specifying enumeration of software installed using system_profiler
- **save**: a boolean flag set to save output to a file
    Note: This argument can only be set with mdfind (output_mdfind.txt) or sp (output_sp.txt)

## Pre-requisites
- A linux-based or darwin-based operating system
- Install necessary dependencies for arguments ie. brew
- Bash shell

## Examples
You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//discovery-and-collection/discover-macOS-software/discover-macOS-software.yaml
```
```bash
ttpforge run forgearmory//discovery-and-collection/discover-macOS-software/discover-macOS-software.yaml \
--arg brew=true
```
```bash
ttpforge run forgearmory//discovery-and-collection/discover-macOS-software/discover-macOS-software.yaml \
--arg mdfind=true
```
```bash
ttpforge run forgearmory//discovery-and-collection/discover-macOS-software/discover-macOS-software.yaml \
--arg mdfind=true --arg save=true
```
```bash
ttpforge run forgearmory//discovery-and-collection/discover-macOS-software/discover-macOS-software.yaml \
--arg sp=true
```
```bash
ttpforge run forgearmory//discovery-and-collection/discover-macOS-software/discover-macOS-software.yaml \
--arg sp=true --arg save=true
```

## Steps
1. **ls_applications_method** (default): This step uses ls to list software installed in the Applications directory.
2. **brew_method**: This step enumerates software installed using brew.
3. **mdfind_method**: This step enumerates software installed using mdfind.
4. **system_profiler_method**: This step enumerates software installed using system_profiler.


## Manual Reproduction Steps
```bash
# Discover installed software in the Applications directory.
ls -la /Applications/

# Discover installed software using brew.
brew list

# Discover installed software using mdfind.
mdfind "kMDItemContentType == 'com.apple.application-bundle'"

# Discover installed software using system_profiler.
system_profiler SPApplicationsDataType

```
## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0007 Discovery
- **Techniques**:
    - T1518 Software Discovery
