# Windows Screen Capture (CopyFromScreen)

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP is designed to take a screen capture of the desktop through a call to the [Graphics.CopyFromScreen] .NET API.
Graphics.CopyFromScreen]: https://docs.microsoft.com/en-us/dotnet/api/system.drawing.graphics.copyfromscreen

Derived from [Atomic Red Team T1113](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1113/T1113.md#atomic-test-6---windows-screen-capture-copyfromscreen)

## Arguments
- **output**: a path variable specifying where captured results will be located. Default is $env:TEMP\T1113.png.

## Pre-requisites
- Windows operating system equipped with powershell

## Examples
You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//collection/capture-screenshot/ttp.yaml
```
```bash
ttpforge run forgearmory//collection/capture-screenshot/ttp.yaml --arg output=png\TTP.png
```

## Steps
1. **copy_from_screen** : This step takes a screen capture of the desktop
2. **cleanup**: Deletes the screen capture that was created

## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0009 Collection
- **Techniques**:
    - T1113 Screen Capture
