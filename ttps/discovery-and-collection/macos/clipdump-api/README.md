# macOS clipboard dump (api)

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP dumps clipboard contents by making nspasteboard API calls.

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
ttpforge run ttps/discovery-and-collection/macos/clipdump-api/clipdump-api.yaml
```

## Steps

1. **clipdump-api**: This step compiles the accompanying Swift code and then
   executes the binary to dump the clipboard content and verify that a specific
   string was captured.

## Accompanying Code

The Swift code used in this TTP interacts with the macOS pasteboard to place
a specific string in the clipboard, then retrieves and verifies that string.

## MITRE ATT&CK Mapping

- **Tactics**:
  - T0009 Collection
- **Techniques**:
  - T1115 Clipboard Data
