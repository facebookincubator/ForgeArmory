# Create Local Account

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP creates a local account for persistence.

## Arguments

- **username**: The name of the username to be created. Default is "evil user".

## Prerequisites

1. The executor must have root access to the system.

## Examples

You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//persistence/linux/create-local-account/create-local-account \
  --arg username=evil_user
```

## Steps

1. **add-evil-user**: This step adds a new local account.
3. **check-success**: This step checks if the user has been successfully added by id command.

## MITRE ATT&CK Mapping

- **Tactics**:
   - TA0003 Persistence
- **Techniques**:
   - T1136 Create Account
- **Subtechniques**:
   - T1053.003 Create Account Local Account
