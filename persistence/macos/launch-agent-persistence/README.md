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
to true, the launch agent and related files will be removed:

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

## Steps

1. **Verify Permissions**: Check that you have the necessary permissions to
   create files in the `~/Library/LaunchAgents` directory and to execute the
   specified script or command.

1. **Create Plist File**: Define a property list file (plist) in
   `~/Library/LaunchAgents` that specifies the script or command to run. The
   plist file will include the `command_or_path` argument, providing details of
   the script or command.

1. **Load Launch Agent**: Use the `launchctl` command to load the plist file.
   This will schedule the execution of the script or command each time the
   system reboots or the user logs in.

1. **Test Execution**: Optionally, test the launch agent to ensure it executes
   the specified script or command as expected.

1. **Cleanup**: If the `cleanup` argument is set to `true`, remove the plist
   file and any related scripts. This will undo the persistence setup, stopping
   the launch agent from executing in the future.
