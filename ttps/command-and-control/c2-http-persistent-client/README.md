# HTTP C2 over persistent connection (client)

## Description
This TTP uses server-sent events (SSE) to establish a single TCP socket that receives continuous data from the server, maintaining a persistent HTTP connection. It simulates a C2 beacon using a persistent HTTP channel.

## Arguments
- **server_host**: Hostname (example.com) or IP address (127.0.0.1) of the server. Defaults to `localhost`.
- **runtime**: Time limit of the connection in seconds. Defaults to `4100`.

## Requirements
1. Linux or macOS platform.
2. Python 3 with the `sseclient` package installed (`pip install sseclient`).

## Examples
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//command-and-control/c2-http-persistent-client/ttp.yaml \
  --arg server_host=c2server.example.com
```

## Steps
1. **dependency_check**: Verifies that the `sseclient` Python package is installed.
2. **execute_client**: Establishes a persistent TCP socket and receives data from the server using server-sent events for the specified runtime duration.
