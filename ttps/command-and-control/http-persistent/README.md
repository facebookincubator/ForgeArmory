# HTTP C2 over persistent TCP connection

## Description
This TTP establishes a simple HTTP C2 beacon connection that is open for at least an hour. It supports two modes: active traffic mode (sends periodic HTTP requests) and passive mode (holds a single TCP connection open using keep-alive).

## Arguments
- **server_host**: Hostname (example.com) or IP address (127.0.0.1) to send requests to. Defaults to `localhost`.
- **max_time**: Connection length in seconds. Defaults to `4000`.
- **interval**: Seconds between HTTP requests (active traffic mode only). Defaults to `5`.
- **traffic**: Whether to send HTTP traffic actively. Defaults to `false`.

## Requirements
1. Linux platform.
2. Python 3 (for active traffic mode) or `nc` (netcat) for passive mode.

## Examples
You can run this TTP with the following command (passive mode):
```bash
ttpforge run forgearmory//command-and-control/http-persistent/ttp.yaml \
  --arg server_host=c2server.example.com
```

Active traffic mode:
```bash
ttpforge run forgearmory//command-and-control/http-persistent/ttp.yaml \
  --arg server_host=c2server.example.com \
  --arg traffic=true \
  --arg interval=10
```

## Steps
1. **client**: Establishes a persistent C2 beacon connection to the server, either by sending periodic HTTP requests (traffic mode) or by holding a single TCP connection open (passive mode).
