# Suspicious Execution via Windows Command Shell

## Description
Demonstrates command execution obfuscation using environment variable substring manipulation. Uses `%LOCALAPPDATA:~-3,1%` to extract "c" from the 3rd character from the end, forming "cmd". This bypasses pattern-matching and string-based detection tools. The test writes and displays a file, showing obfuscated commands still function. Commonly used in fileless malware and living-off-the-land attacks.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **output_file**: File to output to (default: `hello.txt`)
- **input_message**: Message to write to file (default: `Hello, from CMD!`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/suspicious-execution-via-cmd/ttp.yaml \
  --output_file "test.txt" \
  --input_message "Suspicious command executed"
```

## Steps
1. **suspicious_cmd_execution**: Uses environment variable substring manipulation (%LOCALAPPDATA:~-3,1%) to obfuscate the "cmd" command invocation, executes cmd with /c parameter to write the specified message to a file using echo, then displays the file contents using type.
