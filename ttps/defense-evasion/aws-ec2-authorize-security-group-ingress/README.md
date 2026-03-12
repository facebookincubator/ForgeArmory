## TTP
---
This TTP alters the security group of an instance by allowing SSH\RDP access from attacker's IP address.



## Arguments
---
- cidr : Attacker IP Address range
- region
- [optional] protocol
- [optional] port



## Prerequisites
---

1. A valid set of AWS credentials. They can be provided through environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, or AWS_PROFILE.
```
# Set proxy if needed: export https_proxy="http://your-proxy:8080"
```

2. The AWS CLI is installed.


## Example
---
- Run TTP
```bash
ttpforge run forgearmory//defense-evasion/aws-ec2-authorize-security-group-ingress/ttp.yaml  --arg cidr=0.0.0.0/32 --arg region=<region>
```
