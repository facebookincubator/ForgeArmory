# revive-old-iam-user

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

Add a new access key to a previously dormant IAM user.

## Arguments

- **detect:** When set to true, query cloudtrail to determine if the
  TTP was logged.

  Default: true

- **user:** Target IAM user for the new access key.

## Pre-requisites

1. A valid set of AWS credentials. They can be provided through environment
   variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`,
   `AWS_SESSION_TOKEN`, or `AWS_PROFILE`.

1. The AWS CLI is installed.

1. Enumerate user accounts with less than 2 access keys:

  ```bash
  #!/bin/bash

  # List all IAM users
  aws iam list-users --query 'Users[].UserName' --output text | tr '\t' '\n' | while read -r user; do
    # Validate user name
    if [[ "$user" =~ ^[a-zA-Z0-9_=,.@_-]+$ ]]; then
      # List access keys for the user and count them
      ACCESS_KEYS=$(aws iam list-access-keys --user-name "$user" --output json | jq '.AccessKeyMetadata | length')

      if (( ACCESS_KEYS < 2 )); then
        echo "User $user has less than 2 access keys. Current count: $ACCESS_KEYS"
      fi
    else
      echo "Skipping invalid username: $user"
    fi
  done
  ```

## Examples

Create a new access key for the `target-user` IAM user:

```bash
ttpforge run forgearmory//cloud/aws/iam/revive-old-iam-user/revive-old-iam-user.yaml \
  --arg user=target-user
```

## Steps

1. **Ensure AWS Credentials**: Validates if the required AWS credentials are set.

1. **Ensure AWS CLI**: Validates that the AWS Command Line Interface is present
   and executable.

1. **Add Access Key**: Create a new access key for the target IAM user. This
   step also includes the cleanup of any created access key.

1. **Check Detection**: If `detect` is true, query cloudtrail to
   see if the TTP was logged. This step checks for recent `CreateAccessKey`
   and `GenerateDataKey` events.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1098 Account Manipulation
