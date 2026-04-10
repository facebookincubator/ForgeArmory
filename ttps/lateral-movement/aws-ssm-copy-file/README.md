# Copy file over SSM to EC2 instance

## Description
This TTP copies a file to an EC2 instance using AWS Systems Manager (SSM). It creates a temporary SSH configuration, generates an ephemeral key pair, pushes the public key to the instance via SSM, and then uses SCP to transfer the file.

## Arguments
- **ec2_instance_id**: The instance ID of the EC2 instance to copy the file to.
- **aws_region**: The AWS region the EC2 is in. Defaults to `us-west-2`.
- **file_to_copy**: Fully qualified path(s) of the file(s) to be copied, separated by a space.

## Requirements
1. AWS CLI installed and configured with SSM permissions.
2. The target EC2 instance must have the SSM agent running.
3. SSH and SCP must be available on the local machine.

## Examples
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//utils/aws-ssm-copy-file/ttp.yaml \
  --arg ec2_instance_id=i-0123456789abcdef0 \
  --arg file_to_copy=/tmp/payload.bin
```

## Steps
1. **create_ssh_config**: Creates a temporary SSH configuration file to use SSM as a proxy for SSH connections to EC2 instances.
2. **generate_key**: Generates a temporary public/private key pair for authenticating to the EC2 instance.
3. **copy_file_to_ec2**: Pushes the public key to the instance via SSM and copies the file using SCP.
