# Simple macOS E2E Framework Test

## Description
This TTP runs a simple end-to-end framework test using TTPForge on macOS. It executes a base64-encoded Python3 payload that gathers basic system information including hostname, username, and network interface configuration (ifconfig). This is designed to generate an IO for testing purposes.

## Arguments
This TTP takes no arguments.

## Requirements
- Platform: macOS
- Python3 must be installed on the system

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//reconnaissance/e2e-framework-test/ttp.yaml
```

## Steps
1. **python3_b64string**: Executes a base64-encoded Python3 script that runs `hostname`, `id`, and `ifconfig` commands to gather basic system information. Includes a cleanup step that outputs a completion message.
