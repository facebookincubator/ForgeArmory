# Remove Quarantine Attribute

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP leverages xattr and cat to remove the com.apple.quarantine attribute
from a file.

## Pre-requisites

1. The user must have the necessary permissions to access and modify the
   extended attributes of a file.
1. This TTP is specific to macOS, where extended attributes can be managed
   using the `xattr` command.

## Examples

You can run the TTP using the following example:

```bash
ttpforge run forgearmory//defense-evasion/macos/remove-quarantine-attrib/remove-quarantine-attrib.yaml
```

## Steps

1. **setup**: This step creates a zip file for the TTP to use.
1. **xattr-remove-attrib**: This step uses `xattr` to list and remove the
   com.apple.quarantine attribute from the included `Test.app` bundle.
1. **cat-remove-attrib**: This step uses `cat` to remove the
   com.apple.quarantine attribute from the included `Test.zip` archive, and
   provides a cleanup step to delete the temporary file.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0005 Defense Evasion
- **Techniques**:
  - T1553 Subvert Trust Controls
