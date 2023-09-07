# macOS Launch Agent Persistence with Swift

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP creates a launch agent for persistence on macOS. The agent runs a
specified script or command upon system boot or user login.

## Arguments

- **cleanup**:
  When set to true, it removes the launch agent `.plist` and related scripts.
- **command_or_path**:
  Path to the script or bash command for the launch agent to execute.

## Examples

Setup persistence with a script:

```bash
ttpforge run ttps/persistence/macos/launch-agent-persistence/launch-agent-persistence.yaml \
    --arg command_or_path="/Users/Shared/scarybackdoor.sh" \
    --arg cleanup=true
```

Run a direct command:

```bash
ttpforge run ttps/persistence/macos/launch-agent-persistence/launch-agent-persistence.yaml \
    --arg command_or_path="osascript -e 'display dialog \"Hello World\"'" \
    --arg cleanup=true
```

## Steps

1. **launchagent**:
  - Build the `launchagent.swift` source into a compiled binary.
  - Execute the compiled binary. It creates the script at the specified
    path and the `~/Library/LaunchAgents/com.ttpforge.plist` to invoke the
    script. It then loads this agent with `launchctl`.
  - If `cleanup` is set to true, it will:
    1. Delay for 15 seconds before starting the cleanup process.
    1. Use `launchctl` to unload the `.plist`.
    1. Delete the specified script, the `.plist`, and the compiled binary.

## Accompanying Code

The `launchagent.swift` is the core of this TTP:

- It creates a launch agent for the specified command or script.
- For `/Users/Shared/calc.sh`, it launches the Calculator app.
- The script then loads the launch agent with `launchctl`.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1543 Create or Modify System Process
- **Subtechniques**:
  - T1543.001 Create or Modify System Process: Launch Agent
