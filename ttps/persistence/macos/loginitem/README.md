# macOS Login Item Persistence with Swift

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP adds a script or shell command as a Login Item on macOS. The item
will execute each time the user logs in. This method ensures persistence as
the specified command or script runs upon user login.

## Arguments

- **cleanup**: If set to true, the TTP will remove the Login Item and any
  related files, effectively undoing the persistence setup.
- **command_or_path**: Specifies the path to the script or a bash command
  to be executed as a Login Item.

## Examples

Add a specific script as a Login Item using Swift:

```bash
ttpforge run ttps/persistence/macos/login-item/loginitem.yaml \
  --arg command_or_path="/Users/Shared/myScript.sh" \
  --arg cleanup=true
```

Alternatively, run a direct command:

```bash
ttpforge run ttps/persistence/macos/login-item/loginitem.yaml \
  --arg command_or_path="osascript -e 'display dialog \"Hello World\"'" \
  --arg cleanup=true
```

## Steps

1. **loginitem**:
  - Compile the provided `loginitem.swift` source into a binary.
  - Execute the compiled binary. It adds the given command or script to the
    macOS Login Items list, ensuring its execution every time the user logs
    in.
  - If `cleanup` is set to true, it will:
    1. Delay for 15 seconds before initiating the cleanup process.
    1. Remove the login item and associated files.
    1. Revert the persistence.

## Accompanying Code

The `loginitem.swift` script serves as the core functionality behind this
TTP. Upon execution:

- First, it checks if it has been provided with the necessary arguments.
- If the default path `/Users/Shared/calc.sh` is supplied, it creates a
  shell script that opens the Calculator app and sets the appropriate permissions.
- It then attempts to add the provided command or path to the macOS Login
  Items list using JavaScript for Automation (JXA).
- If the cleanup flag is true, it will remove the Login Item using a
  combination of Apple's CoreServices and Security framework functions, as
  well as the SystemConfiguration framework to manage the list of Login Items.
- For the default behavior where the path is `/Users/Shared/calc.sh`, it
  will also delete the created shell script from the filesystem.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1547 Boot or Logon Autostart Execution
- **Subtechniques**:
  - T1547.015 Boot or Logon Autostart Execution: Login Items
