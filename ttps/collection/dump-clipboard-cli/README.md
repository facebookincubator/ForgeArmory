# macOS cli clipboard dump

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP uses the osascript binary to dump clipboard contents.

## Pre-requisites

1. The user must have necessary permissions to execute the `osascript` binary
   and manipulate the clipboard.
1. This TTP is specific to macOS systems.

## Examples

You can run the TTP using the following example:

```bash
ttpforge run forgearmory//collection/dump-clipboard-cli/ttp.yaml
```

## Steps

1. **clipdump-cli**: This step utilizes the `osascript` binary to paste the
   string 'SuperSecretClipboardString' onto the clipboard and then dump the
   clipboard contents. It verifies that the string was obtained and notifies
   if the operation was successful.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0009 Collection
- **Techniques**:
  - T1115 Clipboard Data
