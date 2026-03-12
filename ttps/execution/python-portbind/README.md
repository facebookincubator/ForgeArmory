# Python3 Local Port Binding

## Description
This TTP uses Python3 to listen on a specified local port. It modifies the bundled port-bind.py script to use the specified port, then runs the script in the background for the configured timeout duration.

## Arguments
- **port**: The port to bind to. Default: `8899`
- **timeout**: Timeout value to run the port bind before cleanup. Default: `900`

## Requirements
- Linux operating system

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/python-portbind/ttp.yaml --arg port=9999 --arg timeout=300
```

## Steps
1. **python_bind**: Configure the port-bind.py script with the specified port, launch Python3 to listen on that port in the background, and sleep for the timeout duration. On cleanup, the original contents of port-bind.py are restored.
