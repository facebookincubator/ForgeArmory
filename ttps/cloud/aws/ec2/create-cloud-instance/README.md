# Create new AWS EC2 Instance

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP is used to create a new EC2 instance in AWS. It first checks if default EBS encryption is enabled and disables it if necessary. The instance will be created in the specified region with security settings that by default deny all inbound traffic.
The instance will be tagged for identification and will be terminated during the cleanup process. Default EBS encryption will be restored to its original state during cleanup if it was disabled.

## Arguments
### (create-new-ec2-instance)
  - **instance_name**: Name of the EC2 instance to be created
  - **region**: AWS region where the new EC2 instance will be created.
  - **instance_type**: The type of the new EC2 instance to be created.
  - **ami_id**: The Amazon Machine Image ID used to create the new instance.


## Steps

1. Set up necessary cloud environment variables.
2. Check and disable default EBS encryption if enabled.
3. Verify that a Default VPC is available.
4. Create a new EC2 instance with specified parameters.
5. Wait for the EC2 instance to reach 'running' state.
6. During cleanup, check if the instance is properly initialized before proceeding with its termination.
7. Restore original EBS encryption status if it was modified.

## Manual Reproduction Steps

Check and disable default EBS encryption


`aws ec2 describe-account-attributes --attribute-names "defaultEbsEncryption" --region "REGION"`
`aws ec2 disable-ebs-encryption-by-default --region "REGION"`

Create a new default VPC if it does not exist
`aws ec2 create-default-vpc --region us-west-2 --output text`

Create a new EC2 instance

`aws ec2 run-instances --region "REGION" --image-id "AMI_ID" --instance-type "INSTANCE_TYPE"`

## MITRE ATT&CK Mapping

- **Tactics**:
   TA0005 Defense Evasion
- **Techniques**:
   T1578 Modify Cloud Compute Infrastructure
- **Sub-Techniques**
    T1578.002 Create Cloud Instance
    T1578.003 Delete Cloud Instance
