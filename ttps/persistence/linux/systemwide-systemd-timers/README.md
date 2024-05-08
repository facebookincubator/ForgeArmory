# Systemwide Systemd Timers
## Atomic Tests

- [Method #1 - Create Systemd Service and Timer](#method-1-systemwide-systemd-timers)

- [Method #2 - Create a user transient systemd service and timer](#method-2-systemwide-systemd-timers---transient---user)

- [Method #3 - Create a system level transient systemd service and timer](#method-3-systemwide-systemd-timers---transient---system)

## Method 1: Systemwide Systemd Timers

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP enables the addition of a systemwide systemd timer to run a specified implant.

### Arguments

- **path_to_systemd_service**: The path of the systemd service. Default is /etc/systemd/system/evil.service".
- **path_to_systemd_timer**: The path of the systemd timer. Default is "/etc/systemd/system/evil.timer".
- **systemd_service_name**: The name of the service. Default is "evil.service".
- **systemd_timer_name**: The name of the timer. Default is "evil.timer".
- **implant_name**: The name of the implant to run via the timer. Default is "/bin/touch /tmp/evil-systemd-timers.sh".
- **user**: The user in whose context the systemd service runs.
Default is "root"

### Prerequisites

1. The executor must have root access to the system.

### Examples

You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//persistence/linux/systemwide-systemd-timers/systemd-timers.yaml
```

### Steps

1. **setup**: This step checks if the systemd-run is installed on the current system. If not, the TTP will exit with an error message.
2. **create-systemd-service**: This step creates a new service with the implant payload.
3. **create-systemd-timers**: This step creates a timer and links it with the evil service.
4. **start-systemd-timers**: This step runs starts the timer.
5. **enable-systemd-timers**: This step enables the timer.
6. **systemctl-daemon-reload**: This step forces systemd daemon re-read all the unit files.
7. **check-success**: This step checks if the systemd timer for the specified implant has been successfully created. If so, the TTP will exit with a success message. Otherwise, it will exit with a failure message.

### Manual Reproduction Steps

```
### Escalate privileges to root
sudo su

### Create /etc/systemd/system/evil.service with the following contents:
[Unit]
Description=Evil Systemd Service
[Service]
Type=simple
ExecStart=/bin/touch /tmp/evil-systemd-timers.sh
User=root
[Install]
WantedBy=multi-user.target

### End Create File

### Create /etc/systemd/system/evil.timer with the following contents:
[Unit]
Description=Evil Systemd Timer
Requires=evil.service
[Timer]
Unit=evil.service
OnCalendar=*-*-* *:*:00
[Install]
WantedBy=timers.target

### End Create File

# Start the timer
systemctl start evil.timer

# Automatically start the timer on boot
systemctl enable evil.timer

# Force systemd daemon re-read all the unit files
systemctl daemon-reload

### Clean up: Stop and remove the rogue service and timer

# Stop the timer
systemctl stop evil.timer

# Disable running the timer on boot
systemctl disable evil.timer

# Remove rogue service and timer
rm /etc/systemd/system/evil.service
rm /etc/systemd/system/evil.timer

# Remove the implant file
rm /tmp/evil-systemd-timers.sh
```

## Method 2: Systemwide Systemd Timers - Transient - User

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP enables the addition of a systemwide systemd timer to run a specified implant. This method is transient and does not persist after reboot. It runs on the current user level.

### Arguments

- **systemd_unit_name**: The name of the systemd unit task. Default is "evil".
- **implant_name**: The name of the implant to run via the timer. Default is "/bin/touch /tmp/evil-systemd-timers-transient-user.sh".

### Prerequisites

1. The executor runs as user level on the system.

### Examples

You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//persistence/linux/systemwide-systemd-timers/systemd-timers-transient-user.yaml
```

### Steps

1. **setup**: This step checks if the systemd-run is installed on the current system. If not, the TTP will exit with an error message.
2. **run-transient-systemd-timers-user**: This step runs a scheduled task unit with the implant payload.
7. **check-success**: This step checks if the systemd timer for the specified implant has been successfully created. If so, the TTP will exit with a success message. Otherwise, it will exit with a failure message.

### Manual Reproduction Steps

```
# Run the systemd unit scheduled task command:
systemd-run --user --unit=evil --on-calendar '*:*:0/1' /bin/sh -c '/bin/touch /tmp/systemd-timers-transient-user.sh'

# Wait for 1 minute to allow the scheduled task to complete

### Clean up: Stop the rogue service and timer

# Stop the timer and service
systemctl --user stop evil.timer
systemctl --user stop evil.service

# Remove the implant file
rm /tmp/systemd-timers-transient-user.sh
```


## Method 3: Systemwide Systemd Timers - Transient - System

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP enables the addition of a systemwide systemd timer to run a specified implant. This method is transientt and does not persist after reboot. It runs on the system level.

### Arguments

- **systemd_unit_name**: The name of the systemd unit task. Default is "evil".
- **implant_name**: The name of the implant to run via the timer. Default is "/bin/touch /tmp/evil-systemd-timers-transient-system.sh".

### Prerequisites

1. The executor must have root access to the system.

### Examples

You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//persistence/linux/systemwide-systemd-timers/systemd-timers-transient-system.yaml \
```

### Steps

1. **setup**: This step checks if the systemd-run is installed on the current system. If not, the TTP will exit with an error message.
2. **run-transient-systemd-timers-user**: This step runs a scheduled task unit with the implant payload.
7. **check-success**: This step checks if the systemd timer for the specified implant has been successfully created. If so, the TTP will exit with a success message. Otherwise, it will exit with a failure message.

### Manual Reproduction Steps

```
# Run the systemd unit scheduled task command:
systemd-run --unit=evil --on-calendar '*:*:0/1' /bin/sh -c '/bin/touch /tmp/systemd-timers-transient-user.sh'

# Wait for 1 minute to allow the scheduled task to complete

### Clean up: Stop the rogue service and timer

# Stop the timer and service
systemctl stop evil.timer
systemctl stop evil.service

# Remove the implant file
rm /tmp/systemd-timers-transient-system.sh
```

## MITRE ATT&CK Mapping

- **Tactics**:
   - TA0003 Persistence
- **Techniques**:
   - T1053 Scheduled Task/Job
- **Subtechniques**:
   - T1053.006 Scheduled Task/Job Systemd Timers
