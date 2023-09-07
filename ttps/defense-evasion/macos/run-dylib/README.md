# Run A Dylib

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP executes a C compiled dylib.

## Pre-requisites

1. The code must be executed on a macOS system.
1. The user must have the necessary permissions to compile C and Swift code.
1. macOS Developer tools must be installed as the TTP requires Swift.
   to install developer tools:

    ```bash
    xcode-select --install
    ```

## Examples

You can run the TTP using the following example:

```bash
ttpforge run ttps/defense-evasion/macos/run-dylib/run-dylib.yaml
```

## Steps

1. **rundylib**: This step first compiles the source C file into a dylib,
   then builds the Swift source file to a compiled binary for execution.
   It executes the compiled binary to load the dylib library. If successful,
   the Calculator is loaded.

## Accompanying Code

The TTP includes C and Swift code to compile and run a dylib. The C code
is used to open the Calculator app, while the Swift code handles loading
the compiled dylib.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0002 Execution
- **Techniques**:
  - T1574 Hijack Execution Flow
- **Sub-techniques**:
  - T1574.001 Hijack Execution Flow: DLL Search Order Hijacking
