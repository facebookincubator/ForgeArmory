# Gather macOS system information

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP uses the osascript binary to gather system information on macOS.

## Pre-requisites

1. The system must be running macOS.
1. The user must have the necessary permissions to execute the osascript binary.

## Examples

You can run the TTP using the following example:

```bash
ttpforge run ttps/discovery-and-collection/macos/system-info/system-info.yaml
```

## Steps

1. **system-info**: This step utilizes the `osascript` command to gather system
   information on macOS. The command returns the details of the system
   configuration. Cleanup is not required for this TTP as it simply executes an
   osascript command and does not drop anything to disk.

## MITRE ATT&CK Mapping

- **Tactics**:
  - T0009 Collection
- **Techniques**:
  - T1119 Automated Collection
