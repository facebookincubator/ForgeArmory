# Login Item

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP adds Calc as a Login Item on a macOS system.

## Pre-requisites

1. The code must be executed on a macOS system.
1. The user must have the necessary permissions to add a Login Item.
1. macOS Developer tools must be installed as the TTP requires Swift. To
   install developer tools:

   ```bash
   xcode-select --install
   ```

## Examples

You can run the TTP using the following example:

```bash
ttpforge run ttps/persistence/macos/loginitem/loginitem.yaml
```

## Steps

1. **login-item**: This step first builds the Swift source into compiled
   binaries for adding and removing a Login Item. It then executes the compiled
   `loginitem` binary to add Calc to the Login Items list. The cleanup step
   removes the login item persistence after 15 seconds.

## Accompanying Code

The Swift code used in this TTP consists of two parts:

1. **loginitem.swift**: Adds Calc as a Login Item.
2. **rm-loginitem.swift**: Removes Calculator.app from login items.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1547 Boot or Logon Autostart Execution
- **Subtechniques**:
  - T1547.015 Boot or Logon Autostart Execution: Login Items
