# Apple Remote Desktop using kickstart

## Description
This TTP uses the kickstart command-line tool to enable Apple Remote Desktop (ARD) on the target macOS host. It activates remote management, configures access for all users with all privileges, and then connects to the remote desktop via VNC. The cleanup step deactivates ARD and disables remote access.

## Arguments
This TTP takes no arguments.

## Requirements
- Platform: macOS (darwin)
- Sudo/root privileges are required
- The kickstart tool must be available at `/System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart`

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//utils/enable-remote-desktop/ttp.yaml
```

## Steps
1. **Enabling remote desktop**: Runs the kickstart command with sudo to activate ARD, configure access for all users with all privileges, and restart the ARD agent.
2. **Connecting to remote desktop and cleaning up**: Opens a VNC connection to localhost. The cleanup step waits 3 seconds and then deactivates ARD and disables remote access using the kickstart command.
