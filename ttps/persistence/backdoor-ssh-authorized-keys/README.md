# backdoor-ssh-authorized-keys

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

Add rogue public SSH key to an `authorized_keys` file to maintain
persistence on a target system.

## Arguments

- **ssh_authorized_keys**: Specifies the path to the authorized SSH keys file.
  Defaults to `$HOME/.ssh/authorized_keys`.
- **rogue_key**: Provides the rogue public SSH key to be added. This argument is
  required.
- **post_execution_wait**: Time in seconds to wait after the TTP has executed.
  Defaults to 10 seconds.

## Requirements

Ensure an `authorized_keys` file is present for the user at the specified path or at the default location (`$HOME/.ssh/authorized_keys`).

## Examples

Add a rogue key to the SSH authorized keys. Once execution is
complete, the original `authorized_keys` file is restored:

```bash
ttpforge run forgearmory//persistence/backdoor-ssh-authorized-keys/ttp.yaml \
   --arg ssh_authorized_keys="$HOME/.ssh/authorized_keys" \
   --arg rogue_key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGXY7PWSZ7QafZ5LsBxGVtAcAwn706dJENP1jXlX3fVa Test public key"
```

## Steps

1. **Modify Authorized Keys**: This step takes the provided `rogue_key` argument and appends it to the `authorized_keys` file at the specified or default path. This allows the rogue public SSH key to be used for maintaining persistence on the target system. The original `authorized_keys` file is backed up for potential restoration.

2. **Sleep After Execution**: The TTP waits for the specified `post_execution_wait` time in seconds after execution. This allows for any necessary post-execution actions to complete.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1098: Account Manipulation
- **Subtechniques**:
  - T1098.004: Add or Modify System Process
