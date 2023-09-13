# exfil-instance-profile-creds

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP is designed to extract instance profile credentials from an EC2
instance. This allows you to potentially exfiltrate role-based credentials
that the EC2 instance may have been assigned, enabling broader
access within the AWS environment.

## Arguments

- **detect**: If set to true, the TTP will query AWS GuardDuty to determine if
  the exfiltration was detected.

  Default: true

- **vpc_id**: Specifies the VPC ID. If not provided, it defaults to using the
  default VPC.

- **subnet_id**: Specifies the Subnet ID within the VPC. If not provided,
  it defaults to using the default subnet within the specified or default VPC.

- **security_group_id**: Specifies the Security Group ID. If not provided,
  a new security group with name "ttpforge-exfil-instance-profile-creds-sg"
  and a description "exfil-instance-profile-creds TTP" is created.

  Default: ttpforge-exfil-instance-profile-creds-sg

- **ec2_instance_id**: Specifies the EC2 instance ID. If not provided,
  a new instance will be created.

- **ssh_key**: Specifies the SSH key for accessing the EC2 instance.
  If provided, SSH will be used to extract the instance profile credentials.
  If not provided, the Amazon Systems Manager (SSM) will be used.

## Pre-requisites

1. A valid set of AWS credentials. They can be provided through environment
   variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`,
   `AWS_SESSION_TOKEN`, or `AWS_PROFILE`.

1. The AWS CLI is installed.

1. The `jq` utility must be available for parsing JSON responses from AWS services.

1. For accessing instances, either an SSH key must be provided or the EC2
   instances should have the necessary permissions and setup for using
   Amazon Systems Manager (SSM).

## Examples

Extract instance profile credentials from an EC2 instance within a
specified VPC, Subnet, and EC2 instance using SSM and detect
any exfiltration attempts:

```bash
ttpforge run forgearmory//cloud/aws/ec2/exfil-instance-profile-creds/exfil-instance-profile-creds.yaml \
  --arg vpc_id=vpc-12345678 \
  --arg subnet_id=subnet-12345678 \
  --arg ec2_instance_id=i-12345678
```

Extract instance profile credentials using SSH, specifying an SSH key:

```bash
ttpforge run forgearmory//cloud/aws/ec2/exfil-instance-profile-creds/exfil-instance-profile-creds.yaml \
  --arg vpc_id=vpc-12345678 \
  --arg subnet_id=subnet-12345678 \
  --arg ec2_instance_id=i-12345678 \
  --arg ssh_key=/path/to/ssh_key.pem
```

## Steps

1. **ensure-aws-creds-present**: This step ensures that valid AWS credentials
   are set using environment variables.

1. **ensure-bins-present**: Validates that the relevant binaries to
   execute this TTP are installed on the system.

1. **get-aws-utils**: Downloads a set of AWS utilities which are required for
   subsequent operations.

1. **create-or-use-ec2-and-exfiltrate-instance-profile**: The core step which either
   uses provided AWS resources (like VPC, Subnet, Security Group, EC2 Instance) or
   defaults/creates them. It then attempts to exfiltrate the instance profile
   credentials either using SSH (if an SSH key is provided)
   or Amazon Systems Manager (SSM).

1. **check-detection**: If `detect` is set to true, this step will check
   AWS GuardDuty for findings related to the exfiltration attempt within a
   specified time window. If any findings match the expected type, an alert is raised.
