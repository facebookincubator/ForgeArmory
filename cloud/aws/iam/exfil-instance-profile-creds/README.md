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

## Steps

1. **Preparation**: Ensure a valid set of AWS credentials is available for the
   process to authenticate against AWS services.

2. **Find Default VPC & Subnet**: Locate the default VPC and subnet to be used
   for creating the EC2 instance.

3. **Create Security Group**: Create a security group and authorize inbound
   traffic to control the network traffic for the instance.

4. **Get Latest AMI**: Retrieve the latest Amazon Machine Image (AMI) to be used
   for creating the EC2 instance.

5. **Create EC2 Instance**: Launch an EC2 instance using the identified VPC,
   subnet, security group, and AMI.

6. **Fetch Role Credentials**: Obtain the instance role credentials associated
   with the EC2 instance, and parse the credentials.

7. **Check Role Assumption**: Verify whether the role was assumed successfully
   based on the fetched credentials.

8. **Make API Call**: Attempt to use the obtained credentials to make an API
   call from a non-AWS system, using the role's permissions.

9. **Detection (Optional)**: If `detect` is true, query GuardDuty to determine
   if the TTP was detected.

10. **Cleanup (Optional)**: If `cleanup` is true, remove artifacts created while
    running this TTP, restoring the environment to its prior state.
