# Command Prompt read contents from CMD file and execute

## Description
Demonstrates a command execution technique used by Raspberry Robin malware that leverages `cmd /R <` to read and execute commands from a file via standard input. This approach evades detection by appearing as interactive input rather than script execution. Input redirection pipes CMD file contents into cmd.exe, bypassing monitoring tools that track direct process or file execution. Reference: https://redcanary.com/blog/raspberry-robin/

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **input_file**: CMD file that is read by Command Prompt and execute, which launches calc.exe (default: `./t1059.003_cmd.cmd`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/read-and-execute-cmd-file/ttp.yaml \
  --input_file "C:\Payloads\malicious.cmd"
```

## Steps
1. **ensure_cmd_file_exists**: Verifies that the CMD file exists at the specified path before attempting execution. If the file is not found, the test exits with an error.
2. **execute_cmd_via_stdin**: Uses cmd.exe with the `/r` parameter and input redirection (`<`) to read commands from the specified CMD file and execute them through standard input, simulating the Raspberry Robin malware's execution technique.
