# Red Canary adload detector test

## Description
This TTP tests a Red Canary detector to flag on a curl command observed in adload malware. It starts a local HTTP server, creates a test file, and executes a curl command with JSON payload mimicking adload behavior.

## Arguments
- **timeout**: The amount of time in seconds to run the local HTTP server before auto-exiting. Default: `15`.
- **port**: The local port on which to run the web server. Default: `80`.

## Requirements
- macOS (darwin) platform.
- Python 3 must be installed (used for the HTTP server).

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/adload-trigger/ttp.yaml --arg timeout=20 --arg port=8080
```

## Steps
1. **adload_trigger**: Creates a /tmp/curltest directory with a test file, starts a Python 3 HTTP server on the specified port with the given timeout, then executes a curl POST request with a JSON payload containing parameters typical of adload malware (event, machine_id, URL, OS info, browser agent). During cleanup, it removes the /tmp/curltest directory and its contents.
