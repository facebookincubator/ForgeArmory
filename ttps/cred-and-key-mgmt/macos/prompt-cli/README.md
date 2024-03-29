# macOS cli prompt

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP uses the osascript binary to launch a fake prompt requesting
password entry.

## Arguments

- **detect:** If set to false, the TTP will not check the log file for
  entries indicating the execution of the fake prompt. Default value is `false`.

## Pre-requisites

1. The user must have the necessary permissions to execute the AppleScript
   via the `osascript` binary.
1. This TTP is specific to macOS, where the AppleScript execution can
   be performed.

## Examples

You can run the TTP using the following example:

```bash
ttpforge run forgearmory//cred-and-key-mgmt/macos/prompt-cli/prompt-cli.yaml
```

## Steps

1. **prompt_cli**: This step utilizes the `osascript` command to launch a
   fake authentication prompt that requests password entry and timeouts
   after 10 seconds.
1. **log-prompt-execution**: Logs the execution of the fake authentication
   prompt using the `osascript` binary.
1. **check-detection**: This step checks the log file for entries indicating
   the execution of the fake prompt and reports if any suspicious activity
   is detected.

## MITRE ATT&CK Mapping

- **Tactics**:
  - T1059 Command and Scripting Interpreter
  - TA0006 Credential Access
- **Techniques**:
  - T1059.002 Command and Scripting Interpreter: AppleScript
