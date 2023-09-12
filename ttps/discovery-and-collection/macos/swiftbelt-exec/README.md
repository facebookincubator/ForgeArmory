# Execute SwiftBelt code to gather host information

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP executes SwiftBelt to gather host information on macOS.

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
ttpforge run forgearmory//discovery-and-collection/macos/swiftbelt-exec/swiftbelt-exec.yaml
```

## Steps

1. **swiftbelt-exec**: This step first compiles the SwiftBelt source file into a
   binary for execution, then runs the compiled binary to gather host
   information, and finally cleans up the compiled binary.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0009 Collection
- **Techniques**:
  - T1119 Automated Collection
