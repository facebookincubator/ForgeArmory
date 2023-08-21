# macOS Disable System Updates

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

Disable automatic system security updates.

## Arguments

- **cleanup**: When set to true, it will re-enable automatic system security updates.

## Pre-requisites

Ensure that you have the necessary permissions to write to `/Library/Preferences/com.apple.SoftwareUpdate.plist`.

## Examples

Execute defaults to disable macOS system security updates. Once execution is
complete, this TTP will re-enable automatic system security updates if cleanup is
set to true:

```bash
ttpforge run ttps/defense-evasion/macos/disable-system-updates/disable-system-updates.yaml
```

## Steps

1. **Disable Updates**: Execute defaults to disable automatic system security updates.

1. **Cleanup**: If the `cleanup` argument is set to `true`, execute defaults to enable automatic system security updates.
