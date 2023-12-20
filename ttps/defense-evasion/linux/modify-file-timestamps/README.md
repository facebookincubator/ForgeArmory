# Modify File Timestamps

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP modifies the modify and access timestamps of a file to match another file.

## Arguments

- **escalate_privileges**: Whether or not to escalate privileges before running the TTP. Default is false.
- **target_path**: The path of the target file whose timestamps will be modified. Default is "/etc/passwd".

## Steps

1. ensure-root-user: This step checks if the TTP needs to be run as root user. If so, it ensures that the current user has root privileges. Otherwise, it prints a message indicating that there is no need to run as root.
2. create-copy-of-target: This step creates a copy of the target file in a temporary location. It also cleans up the copy after the TTP execution is complete.
3. change-file-timestamps: This step changes the modify and access timestamps of the target file to match those of the copied file.
4. check-success: This step checks if the TTP was successful by comparing the initial and new information of the target file. If they are different, it indicates that the TTP ran successfully.

## Manual Reproduction Steps

```
# Escalate privileges to root
# (optional - depends on what file you are modifying)
sudo su

# Change this value to the file you are targeting:
TARGET_FILE='/etc/passwd'

# Change this value to the reference file that contains the
# timestamps that you want the $TARGET_FILE to have
REF_FILE='/bin/bash'

# Change the modify and access timestamps of
# $REF_FILE to the timestamps of $TARGET_FILE
touch -acmr "${TARGET_FILE}" "${REF_FILE}"
```

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0005 Defense Evasion
- **Techniques**:
  - T1070.006 Indicator Removal
- **Subtechniques**:
  - T1070.006 Indicator Removal Timestomp
