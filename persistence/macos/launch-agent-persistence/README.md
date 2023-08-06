# macOS Launch Agent Persistence

Create and manage a launch agent on macOS, allowing for persistent execution of a
given script or command. The launch agent will execute the specified script or
command each time the system reboots or the user logs in.

## Arguments

- **command_or_path**: This argument specifies the path to the script or a bash
  command to be run by the launch agent.

- **cleanup**: When set to true, it will remove the launch agent plist file and
  any related scripts, undoing the persistence setup.

## Pre-requisites

Ensure that you have the necessary permissions to create files in the user's
`~/Library/LaunchAgents` directory and execute the specified script or command.

## Examples

Set up launch agent persistence with a specific script. The agent will execute
the script every time the system reboots or the user logs in. If cleanup is set
to true, the launch agent and related files will be removed after 3 minutes:

```bash
ttpforge -c config.yaml \
    run ttps/persistence/macos/launch-agent-persistence/launch-agent-persistence.yaml \
    --arg command_or_path="/Users/Shared/scarybackdoor.sh" \
    --arg cleanup=true
```

Alternatively, you can use a direct bash command:

```bash
ttpforge -c config.yaml \
    run ttps/persistence/macos/launch-agent-persistence/launch-agent-persistence.yaml \
    --arg command_or_path="bash -c echo Oh uh" \
    --arg cleanup=true
```
