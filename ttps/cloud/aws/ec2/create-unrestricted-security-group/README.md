# Create Unrestricted Security Group

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP (Tactic, Technique, and Procedure) creates an unrestricted security
group in AWS. It sets up a security group that allows all inbound traffic
across all ports and protocols.

## Arguments

- **detect**: Detect unrestricted security group access.
  Default: true

- **region**: Region to create the unrestricted security group in.
  Default: us-east-1

- **sg_name**: Prefix name of the security group to create.
  Default: unrestricted-sg

- **vpc_id**: VPC ID to create the unrestricted security group in. If not
  provided, the default VPC is used.
  Default: nil

- **wait_detect_time**: Time to wait for AWS GuardDuty to detect the event.
  Default: 30

## Requirements

1. AWS CLI must be installed and properly configured.
1. Sufficient AWS permissions to create and manage security groups.
1. Dependencies listed in the script must be resolved.
1. jq must be installed for JSON parsing.

## Examples

You can run the TTP using the following example command (adjust arguments as
needed):

```bash
ttpforge run forgearmory//cloud/aws/ec2/create-unrestricted-security-group/create-unrestricted-security-group.yaml
```

## Steps

1. **aws-connector**: This step invokes the setup_cloud_env action to ensure
   the AWS environment is configured.

1. **create-unrestricted-security-group**: Creates an unrestricted security
   group in AWS. The group name includes a random string to ensure uniqueness.

1. **wait-detection**: Waits for the specified time to allow AWS GuardDuty and
   CloudTrail to detect the event.

1. **check-detection**: Checks if AWS GuardDuty or CloudTrail detected the
   event within the specified time frame.

## MITRE ATT&CK Mapping

- **Tactics**:

  - TA0005 Defense Evasion
  - TA0006 Credential Access

- **Techniques**:

  - T1078 Valid Accounts
  - T1190 Exploit Public-Facing Application

- **Sub-Techniques**:
  - T1087.002 AWS Account
