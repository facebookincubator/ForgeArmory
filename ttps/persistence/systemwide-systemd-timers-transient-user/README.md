# Systemd Timer Persistence (Transient User-Level)

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP creates a user-level systemd timer for persistence on Linux
systems. The timer is transient and will not persist after system
reboot, making it useful for temporary persistence scenarios or testing.

## Arguments

- **systemd_unit_name**: Name of the systemd unit (default: `evil`)
- **implant_name**: Path to the file that the timer will create/touch
  (default: `/tmp/evil-systemd-timers-transient-user.sh`)

## Prerequisites

1. The system must have `systemd-run` installed
2. User-level systemd timers must be supported on the system

## Examples

Run with default settings:

```bash
ttpforge run forgearmory//persistence/systemwide-systemd-timers-transient-user/ttp.yaml
```

Run with custom unit name and implant path:

```bash
ttpforge run forgearmory//persistence/systemwide-systemd-timers-transient-user/ttp.yaml \
    --arg systemd_unit_name=my-timer \
    --arg implant_name=/tmp/my-implant.sh
```

## Steps

1. **setup**: Verifies that `systemd-run` is installed on the system
2. **run-transient-systemd-timers-user**: Creates a transient user-level
   systemd timer that executes every minute to touch the specified file
   - Waits 70 seconds to allow the timer to execute
   - Cleanup: Stops the timer service and timer, then reloads systemd
3. **check-success**: Verifies that the implant file was created by the
   timer
   - Cleanup: Removes the implant file

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1053 Scheduled Task/Job
- **Subtechniques**:
  - T1053.006 Scheduled Task/Job: Systemd Timers
