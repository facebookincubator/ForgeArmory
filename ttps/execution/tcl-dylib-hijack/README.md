# Load a dylib using tclsh

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP loads a custom dylib (which opens Calculator) by piping an echo
command to tclsh.

## Pre-requisites

1. The user must have the necessary permissions to build and load the dylib.
1. This TTP is specific to macOS systems where `tclsh` and `gcc` are available.

## Accompanying Code

The C code used in this TTP builds a dynamic library that opens the
Calculator app when loaded. The code is compiled into a dylib using the gcc
compiler and loaded using tclsh.

## Examples

You can run the TTP using the following example:

```bash
ttpforge run forgearmory//execution/tcl-dylib-hijack/ttp.yaml
```

## Steps

1. **tcl-load-dylib**: This step first builds the source C file into a dylib,
   then uses tclsh to load the dylib. If the Calculator application is found
   running, it confirms the successful loading of the dylib.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0002 Execution
- **Techniques**:
  - T1574 Hijack Execution Flow
- **Sub-techniques**:
  - T1574.001 Hijack Execution Flow: DLL Search Order Hijacking
