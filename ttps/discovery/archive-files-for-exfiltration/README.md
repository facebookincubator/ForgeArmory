# Compress for Exfil

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP archives files with a specific extension in the specified directory
for exfiltration.

## Arguments

- **escalate_privileges**: Whether to escalate privileges to root user before
  running the TTP

  Default: false

- **starting_dir**: The starting directory to search for files

  Default: /usr/include/sound/

- **file_ext**: The file extension to archive

  Default: h

- **tar_path**: The path to save the tar file

  Default: exfil.tar

## Steps

1. Ensure that the TTP is being run as root user, if required.
1. Archive files with the specified extension in the specified directory using
   the `find` and `tar` commands.
1. Check if the tar file was successfully created. If not, exit with an error
   message. Otherwise, exit with a success message.

## Manual Reproduction Steps

```bash
# Escalate privileges to root
# (optional - depends on what directories you're looking in)
sudo su

find /etc/chef -type f -name "*.json" -exec tar -rvf /tmp/all-chef-json-files.tar "{}" \;
```

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0007 Discovery
  - TA0009 Collection
- **Techniques**:
  - T1083 File and Directory Discovery
  - T1005 Data from Local System
