# Inject Dylib

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP injects a custom dylib (which opens Calculator) into the
SafariForWebkitDevelopment binary.

## Pre-requisites

1. The code must be executed on a macOS system.
1. The user must have the necessary permissions to access the TCC folder and
   compile Swift code.
1. macOS Developer tools must be installed as the TTP requires Swift. To
   install developer tools:

   ```bash
   xcode-select --install
   ```

## Examples

You can run the TTP using the following example:

```bash
ttpforge run forgearmory//defense-evasion/macos/injectdylib/injectdylib.yaml
```

## Steps

1. **inject-dylib**: This step compiles and links the source code into a
   dynamic library, and then uses `DYLD_INSERT_LIBRARIES`` to inject the
   library into SafariForWebkitDevelopment.
   A cleanup step removes the compiled binaries after execution.

## Accompanying Code

The Swift code used in this TTP attempts to inject a dylib into
`/Applications/Safari.app/Contents/MacOS/SafariForWebkitDevelopment`.

The C code includes a custom constructor that runs a command to open
the Calculator app.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0005 Defense Evasion
- **Techniques**:
  - T1055 Process Injection
