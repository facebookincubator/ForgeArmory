# macOS API Prompt

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP uses the osascript library (via API calls) to launch a fake
authentication prompt.

## Pre-requisites

1. The code must be executed on a macOS system.
1. The user must have the necessary permissions to access the TCC folder and
   compile Swift code.
1. macOS Developer tools must be installed as the TTP requires Swift. To install
   developer tools:

   ```bash
   xcode-select --install
   ```

## Examples

You can run the TTP using the following example:

```bash
ttpforge run forgearmory//execution/user-prompt-api/ttp.yaml
```

## Steps

1. **prompt-api**: This step builds a Swift binary file and executes it to
   display a fake authentication prompt. The compiled binary is deleted after
   execution.

## Accompanying Code

The Swift code used in this TTP launches a fake authentication prompt using
AppleScript, capturing the user's credentials if entered.

## MITRE ATT&CK Mapping

- **Tactics**:
  - T1059 Command and Scripting Interpreter
  - TA0006 Credential Access
- **Techniques**:
  - T1059.002 Command and Scripting Interpreter: AppleScript
