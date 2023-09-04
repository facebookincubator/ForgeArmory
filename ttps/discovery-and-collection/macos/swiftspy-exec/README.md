# Execute SwiftSpy to perform keylog monitoring

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP executes SwiftSpy to monitor keyboard strokes.

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
ttpforge run ttps/discovery-and-collection/macos/swiftspy-exec/swiftspy-exec.yaml
```

## Steps

1. **swiftspy-exec**: This step first compiles the SwiftSpy source file into a
   binary and then executes it with a 20-second timeout. If there are any issues
   with permissions, it will notify the user.

## Accompanying Code

The Expect script used in this TTP is responsible for spawning a bash shell
and executing the compiled SwiftSpy binary.

## MITRE ATT&CK Mapping

- **Tactics**:
  - T0009 Collection
- **Techniques**:
  - T1056 Input Capture
- **Subtechniques**:
  - T1056.001 Input Capture: Keylogging
