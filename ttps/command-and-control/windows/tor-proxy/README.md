# Tor Proxy Usage - Windows

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP is designed to launch the tor proxy service, which is what is utilized in the background by the Tor Browser and other applications with add-ons in order to provide onion routing functionality. Upon successful execution, the tor proxy will be launched, run for 60 seconds, and then exit.

Derived from [Atomic Red Team T1090.003](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1090.003/T1090.003.md#atomic-test-2---tor-proxy-usage---windows)

## Arguments
- **torExe**: a string variable specifying the location of tor.exe (including dependencies). Default is "$PWD\bin\Tor\tor.exe".
- **sleepTime** : an int variable specifying the amount in seconds to pause after starting tor

## Pre-requisites
- Windows operating system equipped with powershell

## Examples
You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//command-and-control/windows/tor-proxy/tor-proxy.yaml
```
```bash
ttpforge run forgearmory//command-and-control/windows/tor-proxy/tor-proxy.yaml --arg torExe=Tor\tor.exe
```
```bash
ttpforge run forgearmory//command-and-control/windows/tor-proxy/tor-proxy.yaml --arg sleepTime=30
```

## Steps
1. **tor_execute** : This step installs tor.exe, if not provided, and executes the binary
2. **cleanup**: Stops the process for tor.exe then removes bin\Tor if it was downloaded

## Manual Reproduction
```bash
#Run bin\Tor\tor.exe
bin\Tor\tor.exe

#Wait for tor to fully set up
start-sleep -Seconds 60

#Stop tor process
stop-process -name "tor" | out-null

```

## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0011 Command and Control
- **Techniques**:
    - T1090 Proxy
- **Subtechniques**:
    - T1090.003 Multi-hop Proxy
