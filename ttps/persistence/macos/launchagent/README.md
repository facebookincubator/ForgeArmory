# macOS Launch Agent Persistence with Swift Support

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP creates a launch agent that executes a given shell command or a
compiled Swift binary for persistence on macOS. The launch agent will execute
the specified script or command each time the system reboots or the user logs
in.

## Arguments

- **cleanup**: When set to true, it will remove the launch agent plist
  file and any related scripts, undoing the persistence setup.
- **command_or_path**: This argument specifies the path to the script
  or a bash command to be run by the launch agent.

## Examples

Set up launch agent persistence with a specific script, using Swift:

```bash
ttpforge run ttps/persistence/macos/launch-agent-persistence/launch-agent-persistence.yaml \
    --arg command_or_path="/Users/Shared/scarybackdoor.sh" \
    --arg cleanup=true
```

Alternatively, without Swift:

```bash
ttpforge run ttps/persistence/macos/launch-agent-persistence/launch-agent-persistence.yaml \
    --arg command_or_path="bash -c echo Oh uh" \
    --arg cleanup=true
```

## Steps

### Shell-based Path

1. **Create LaunchAgents Directory**: If not already present, the directory
   `~/Library/LaunchAgents` will be created to store the plist file.
2. **Write Plist File**: A plist file will be written to
   `~/Library/LaunchAgents/com.ttpforge.plist`. It defines how the launch agent
   will execute the command specified in the `command_or_path` argument.
3. **Activate Launch Agent**: The plist is set to activate on the next reboot,
   providing persistence for the given command or script.

### Swift-based Path

1. **Compile Swift Code**: If `use_swift` is set to true, the Swift code is
   compiled into a binary.
2. **Execute Swift Binary**: The compiled binary is executed, performing the
   same steps as the shell-based path but with additional possibilities
   provided by Swift, such as more complex error handling or additional
   functionality.

### Cleanup Step

1. **Cleanup**: If the `cleanup` argument is set to `true`,
   the `launchctl` command is used to unload the plist, and all related
   files are deleted. This reverses the persistence setup.

## MITRE ATT&CK Mapping

- **Tactics**:
  - T0003 Persistence
- **Techniques**:
  - T1543 Create or Modify System Process
- **Subtechniques**:
  - T1543.001 Create or Modify System Process: Launch Agent
