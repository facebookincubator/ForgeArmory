# Protocol Tunneling SSH

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP enables the creation of an SSH tunnel to fetch a file from a remote system.

## Arguments
- **target_path**: The path where the webserver will be started and the file will be written. Default is "/tmp/webserver".
- **target_port**: The port where the webserver will listen. Default is "8000".
- **local_port**: The local port where the SSH tunnel will be created. Default is "3333".
- **target_user**: The user with which to connect to the target system. Default is "root".
- **target_server**: The IP address or hostname of the target system. Default is "localhost".

## Pre-requisites

1. The target system must have Python3 and curl installed.
2. The target system must allow incoming connections on the specified target_port.
3. The executor must have SSH access to the target system as the specified target_user (public key).

## Examples

You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//command-and-control/protocol-tunneling-ssh.yaml \
  --arg target_path=/tmp/webserver --arg target_port=8000 --arg local_port=3333 --arg target_user=root --arg target_server=localhost
```

## Steps

1. **setup**: This step verifies that the required software is present.
2. **create-target-directory**: This step creates the target directory if it does not exist.
3. **write-file-to-target-directory**: This step writes a file named "FOUNDME" to the target directory.
4. **execute-ssh-tunneling**: This step starts a webserver on the target system, sets up an SSH tunnel to the target system, and fetches the "FOUNDME" file through the tunnel. If the file is found, the TTP execution is successful. Otherwise, it fails.

## Manual Reproduction Steps

```
### Target Configuration

# Escalate privileges to root
# (optional - depends on the goal(s) of your simulation)
sudo su

TEMP_SIM_DIR=/tmp/bla

mkdir "${TEMP_SIM_DIR}"
echo 'you found me' >> "${TEMP_SIM_DIR}/FOUNDME"

# Start webserver
pushd "${TEMP_SIM_DIR}" || exit
timeout 60 python3 -m http.server 8080
popd || exit

### Attacker Configuration
TARGET_USER="jaysong"
TARGET_SERVER="devvm3704.vll0.facebook.com"
ssh -L 8080:localhost:8080 "${TARGET_USER}@${TARGET_SERVER}"

# Check the output of this command for FOUNDME
curl localhost:8080

# Clean up
rm -rf /tmp/bla
```

## MITRE ATT&CK Mapping

- **Tactics**:
   - TA0011 Command and Control
- **Techniques**:
   - T1572 Protocol Tunneling
