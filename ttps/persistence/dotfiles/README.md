# Create .zshrc Persistence

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP checks the presence of the `~/.zshrc` file on the target system.
If it is absent, this TTP creates it and appends a specified command or
script for execution whenever the `.zshrc` is sourced (typically on shell
startup).

## Arguments

- **command**: Specifies the command that will be executed upon
  sourcing `.zshrc`.
  Default: `uname -a > /tmp/system-info.txt`

## Pre-requisites

1. The user must have the necessary permissions to access and modify
   the `.zshrc` file.

2. The TTP is specific to systems using the Z shell (`zsh`).

## Examples

To run the TTP with its default settings:

```bash
ttpforge run forgearmory//persistence/dotfiles/persist-zshrc.yaml
```

To specify a custom command:

```bash
ttpforge run forgearmory//persistence/dotfiles/persist-zshrc.yaml \
  --arg command="echo 'Hello, World!' > /tmp/hello.txt"
```

## Steps

1. **zshrc**: This step first checks for the existence of `~/.zshrc`.
   If it isn't found, the file is created. Subsequently, it appends a
   specified command to the `.zshrc` file, ensuring its execution whenever
   the file is sourced. It also creates a temporary shell script,
   `ttpforge-persist-zshrc.sh`, to assist in the persistence. A backup of
   the original `.zshrc` is also created as `.zshrc-orig`.

   Unless `--no-cleanup` is set, the original `~/.zshrc` file is
   restored.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1547 Boot or Logon Autostart Execution
- **Subtechniques**:
  - T1547.007 Boot or Logon Autostart Execution: Re-opened Applications
