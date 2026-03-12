# Keylogger using Obj-C

## Description
This TTP creates a keylogger binary using Objective-C and executes it to capture the first 20 keystrokes on a macOS system. The keylogged data is stored to a file on disk.

## Arguments
This TTP takes no arguments.

## Requirements
- macOS (darwin) platform
- `clang` compiler must be available
- Cocoa and Carbon frameworks must be available

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//credential-access/keylogger-objc/ttp.yaml
```

## Steps
1. **Create keylogger binary**: Compiles the `keylogger.m` Objective-C source file using `clang` with the Cocoa and Carbon frameworks, then executes the compiled binary to capture keystrokes. During cleanup, both the compiled binary and the captured keystroke data at `/tmp/keys.txt` are removed.
