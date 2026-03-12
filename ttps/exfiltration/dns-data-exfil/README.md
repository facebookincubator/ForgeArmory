# Data exfiltration over DNS records

## Description
This TTP takes a file over 100kB in size and exfiltrates it in chunks (63 characters) over DNS A or TXT records. It simulates data exfiltration over an alternative, unencrypted protocol.

## Arguments
- **domain**: The domain to use for DNS data exfiltration. Defaults to `example.com`.
- **dns**: IP address of the DNS server. Defaults to `127.0.0.1`.
- **type**: DNS query type (`A` or `TXT`). Defaults to `A`.

## Requirements
1. Linux or macOS platform.
2. `dig` must be available on the system.
3. `openssl` for generating the test file.
4. A DNS server running at the specified address to receive the exfiltrated data.

## Examples
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//exfiltration/dns-data-exfil/ttp.yaml \
  --arg domain=example.com \
  --arg dns=10.0.0.1
```

Using TXT records:
```bash
ttpforge run forgearmory//exfiltration/dns-data-exfil/ttp.yaml \
  --arg domain=example.com \
  --arg dns=10.0.0.1 \
  --arg type=TXT
```

## Steps
1. **generate_file**: Generates a random 100kB file for exfiltration.
2. **exfil_data**: Sends the file content in 63-character chunks as DNS subdomain queries to the specified server. Cleans up the generated file on completion.
