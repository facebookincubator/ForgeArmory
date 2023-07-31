# exfil-instance-profile-creds

Finds the default VPC and subnet, creates a security group,
authorizes inbound traffic, gets the latest AMI, creates an EC2 instance,
and fetches the instance role credentials.

It then parses the credentials and checks whether the role was
assumed successfully.

It will then attempt to use the credentials to make an API call from
a non-aws system.

## Arguments

- detect: When set to true, query GuardDuty to determine if the
  TTP was detected.

- cleanup: When set to true, attempt to clean up the artifacts created
  while running this TTP.

## Pre-requisites

A valid set of AWS credentials.

## Examples

Create a new ec2 instance with SSM, exfil the instance profile, and
attempt to use it on a non-AWS system.

```bash
./ttpforge -c config.yaml \
    run ttps/cloud/aws/iam/exfil-instance-profile-creds/exfil-instance-profile-creds.yaml \
    --arg cleanup=true \
    --arg detect=true
```
