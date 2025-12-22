# Systemd Timer Persistence (System-Wide)

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP creates a system-wide systemd timer for persistence on Linux
systems. Unlike the transient variant, this timer persists across system
reboots by creating service and timer unit files in
`/etc/systemd/system/`.

## Arguments

- **path_to_systemd_service**: Path where the service file will be
  created (default: `/etc/systemd/system/evil.service`)
- **path_to_systemd_timer**: Path where the timer file will be created
  (default: `/etc/systemd/system/evil.timer`)
- **systemd_service_name**: Name of the systemd service (default:
  `evil.service`)
- **systemd_timer_name**: Name of the systemd timer (default:
  `evil.timer`)
- **implant_name**: Path to the file that the timer will create/touch
  (default: `/tmp/evil-systemd-timers.sh`)
- **user**: User context in which the service runs (default: `root`)

## Prerequisites

1. Root/superuser privileges are required
2. The system must have systemd installed

## Examples

Run with default settings (requires sudo):

```bash
sudo ttpforge run forgearmory//persistence/systemwide-systemd-timers/ttp.yaml
```

Run with custom service and timer names:

```bash
sudo ttpforge run forgearmory//persistence/systemwide-systemd-timers/ttp.yaml \
    --arg systemd_service_name=my-service.service \
    --arg systemd_timer_name=my-service.timer \
    --arg implant_name=/tmp/my-implant.sh
```

Run as a specific user:

```bash
sudo ttpforge run forgearmory//persistence/systemwide-systemd-timers/ttp.yaml \
    --arg user=nobody \
    --arg implant_name=/tmp/nobody-implant.sh
```

## Steps

1. **setup**: Verifies that `systemd-run` is installed on the system
2. **create-systemd-service**: Creates the systemd service unit file
   that touches the implant file
   - Cleanup: Removes the service file
3. **create-systemd-timers**: Creates the systemd timer unit file
   configured to run every minute
   - Cleanup: Removes the timer file
4. **start-systemd-timers**: Starts the systemd timer
   - Cleanup: Stops the timer
5. **enable-systemd-timers**: Enables the timer to start on boot
   - Cleanup: Disables the timer and reloads systemd daemon
6. **systemctl-daemon-reload**: Reloads the systemd daemon and waits 5
   seconds
7. **check-success**: Verifies that the implant file was created
   - Cleanup: Removes the implant file

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1053 Scheduled Task/Job
- **Subtechniques**:
  - T1053.006 Scheduled Task/Job: Systemd Timers
