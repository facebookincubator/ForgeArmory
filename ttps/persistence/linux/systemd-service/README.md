# Systemd Service

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP creates a rogue systemd service to run a command as the linux user.

## Arguments

- **user**: The user in whose context the systemd service runs.

## Prerequisites

1. The executor must have root access to the target machine.

## Examples
You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//persistence/linux/systemd-service/systemd-service.yaml
```

## Steps

1. **create-rogue-service**: This step creates a new systemd service file named "evil.service" in the "/etc/systemd/system/" directory. The service file contains the necessary configuration to run the specified command as the specified user (default: root).
2. **start-rogue-service**: This step starts the newly created "evil" service.
3. **enable-rogue-service-on-boot**: This step enables the "evil" service to start automatically on boot.

## Manual Reproduction Steps

```
### Escalate privileges to root
sudo su

### Create /etc/systemd/system/evil.service with the following contents:
[Unit]
Description=Evil service
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=centos
ExecStart=echo 'this could be something bad'

[Install]
WantedBy=multi-user.target

### End Create File

# Start the service
systemctl start evil

# Automatically start the service on boot
systemctl enable evil

### Clean up: Stop and remove the rogue service

# Stop the service
systemctl stop evil

# Disable running the service on boot
systemctl disable evil

# Remove rogue service
rm /etc/systemd/system/evil.service
```

## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0003 Persistence
- **Techniques**:
    - T1543 Create or Modify System Process
- **Subtechniques**:
    - T1543.002 Create or Modify System Process Systemd Service
