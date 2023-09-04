# Local Network Service Discovery

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP runs different dns-sd commands for local network service discovery.

## Pre-requisites

1. The user must have the necessary permissions to run the dns-sd commands.
1. This TTP is specific to macOS.

## Examples

You can run the TTP using the following example:

```bash
ttpforge run ttps/discovery-and-collection/macos/service-discovery/service-discovery.yaml
```

## Steps

1. **discover-ssh-hosts**: This step searches for hosts serving ssh via dns-sd.
1. **discover-web-hosts**: This step searches for hosts serving web services via
   dns-sd.
1. **discover-remote-screen-sharing-hosts**: This step searches for hosts
   serving remote screen sharing via dns-sd.
1. **discover-smb-hosts**: This step searches for hosts serving smb via dns-sd.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0043 Reconnaissance
- **Techniques**:
  - T1592 Gather Victim Host Information
