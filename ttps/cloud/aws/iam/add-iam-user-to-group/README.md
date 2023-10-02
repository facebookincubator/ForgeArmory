# Add IAM User to Group

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP enables the addition of a specified IAM user to a specified user
group in AWS.

## Arguments

- **user**: The IAM user to add to an IAM user group.

- **group**: The IAM user group to add the input IAM user to.

## Pre-requisites

1. AWS credentials must be present either through environment variables
   (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and optionally
   `AWS_SESSION_TOKEN`) or an AWS profile set with `AWS_PROFILE`.
1. The AWS CLI must be installed and accessible.
1. The executor must have IAM permissions to add and remove users from IAM
   groups.

## Examples

You can run the TTP using the following example (after updating the arguments):

```bash
ttpforge run forgearmory//cloud/aws/iam/add-iam-user-to-group/add-iam-user-to-group.yaml \
  --arg user=myiamuser --arg group=myiamgroup
```

## Steps

1. **ensure-aws-creds-present**: This step ensures AWS credentials are
   appropriately set and configured before the TTP's execution.
1. **ensure-aws-cli-present**: This step checks for the presence of the AWS
   CLI on the system and provides feedback on its version.
1. **add-user-to-group**: This step adds the specified user to the specified
   user group. Additionally, a cleanup step is provided to remove the user
   from the group post-execution.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1098 Account Manipulation
