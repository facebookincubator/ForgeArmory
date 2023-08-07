# backdoor-ssh-authorized-keys

Add rogue public SSH key to an `authorized_keys` file to maintain persistence
on a target system.

## Arguments

- ssh_authorized_keys: This argument specifies the path to the authorized SSH
  keys file. If none is provided, it defaults to $HOME/.ssh/authorized_keys.

- rogue_key: This argument provides the rogue public SSH key to be added.

- cleanup: When set to true, it will restore the original authorized_keys file
  from a backup created during the execution of the script.

## Pre-requisites

Ensure an authorized_keys file is present for the user at the path
specified, or at the default location (`$HOME/.ssh/authorized_keys`).

## Examples

Add a rogue key to the SSH authorized keys. Once execution is
complete, the original authorized_keys file is restored if cleanup is
set to true:

```bash
ttpforge -c config.yaml \
    run ttps/persistence/ssh/backdoor-authorized-keys/backdoor-authorized-keys.yaml \
    --arg ssh_authorized_keys="$HOME/.ssh/authorized_keys" \
    --arg rogue_key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGXY7PWSZ7QafZ5LsBxGVtAcAwn706dJENP1jXlX3fVa Test public key" \
    --arg cleanup=true
```

## Steps

1. **Setup**: Checks for the presence of the `authorized_keys` file at the
   specified path or at the default location (`$HOME/.ssh/authorized_keys`).
   If absent, an error message is displayed and the script exits. If present,
   it backs up the original file for potential restoration.

1. **Add Rogue Key**: Takes the provided `rogue_key` argument and appends it
   to the `authorized_keys` file at the specified or default path. This
   allows the rogue public SSH key to be used for maintaining persistence
   on the target system.

1. **Cleanup**: If the `cleanup` argument is set to `true`, the script
   restores the original `authorized_keys` file from the backup created
   during the execution of the script. This will remove the rogue key and
   revert the file to its original state.
