# backdoor-ssh-authorized-keys

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

Add rogue public SSH key to an `authorized_keys` file to maintain
persistence on a target system.

## Arguments

- **ssh_authorized_keys**: This argument specifies the path to the
  authorized SSH keys file. If none is provided, it defaults to
  `$HOME/.ssh/authorized_keys`.

- **rogue_key**: This argument provides the
  rogue public SSH key to be added.

## Pre-requisites

Ensure an authorized_keys file is present for the user at the path
specified, or at the default location (`$HOME/.ssh/authorized_keys`).

## Examples

Add a rogue key to the SSH authorized keys. Once execution is
complete, the original authorized_keys file is restored:

```bash
ttpforge run forgearmory//persistence/ssh/backdoor-ssh-authorized-keys/backdoor-ssh-authorized-keys.yaml \
   --arg ssh_authorized_keys="$HOME/.ssh/authorized_keys" \
   --arg rogue_key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGXY7PWSZ7QafZ5LsBxGVtAcAwn706dJENP1jXlX3fVa Test public key"
```

## Steps

1. **Setup**: Checks for the presence of the `authorized_keys` file at the
   specified path or at the default location (`$HOME/.ssh/authorized_keys`).
   If absent, an error message is displayed and the TTP exits. If present,
   it backs up the original file for potential restoration.

1. **Add Rogue Key**: Takes the provided `rogue_key` argument and appends it
   to the `authorized_keys` file at the specified or default path. This
   allows the rogue public SSH key to be used for maintaining persistence
   on the target system. Unless `--no-cleanup` is set, the original
   `authorized_keys` file is restored.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1098: Account Manipulation
- **Subtechniques**:
  - T1098.004: Add or Modify System Process
