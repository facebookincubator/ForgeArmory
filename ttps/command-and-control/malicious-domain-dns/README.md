# Malicious Domain DNS

## Description
This TTP mimics a macOS user trying to find the DNS record for a malicious domain. It uses the `dig` command to perform a DNS lookup against the specified domain.

## Arguments
- **domain**: The domain to query. Default: `00bca37b237615ab.fun`

## Requirements
- macOS (darwin) platform
- `dig` command must be available

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//command-and-control/malicious-domain-dns/ttp.yaml --arg domain=example.com
```

## Steps
1. **Lookup DNS record for malicious domain**: Executes `dig` with the specified domain to perform a DNS lookup and display the results.
