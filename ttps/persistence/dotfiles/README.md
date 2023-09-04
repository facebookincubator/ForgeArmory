# Create .zshrc Persistence

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP checks to see if `~/.zshrc` is present and if not creates it and adds
a line to execute a script (which opens Calc).

## Pre-requisites

1. The user must have the necessary permissions to access and create the
   `.zshrc` file.
1. This TTP is specific to systems using the Zsh shell.

## Examples

You can run the TTP using the following example:

```bash
ttpforge run ttps/persistence/dotfiles/persist-zshrc.yaml
```

## Steps

1. **zshrc**: This step checks if `~/.zshrc` is present. If not, it creates
   the file and appends a line to execute a script, which opens the Calculator
   app. It also provides a cleanup step to remove any added changes.

## MITRE ATT&CK Mapping

- **Tactics**:
  - T0003 Persistence
- **Techniques**:
  - T1547 Boot or Logon Autostart Execution
- **Subtechniques**:
  - T1547.007 Boot or Logon Autostart Execution: Re-opened Applications
