# revive-old-iam-user

Add a new access key to a previously dormant IAM user.

## Arguments

- detect: When set to true, query cloudtrail to determine if the
  TTP was logged.

- cleanup: When set to true, attempt to clean up the artifacts created
  while running this TTP.

- user: Target IAM user for the new access key.

## Pre-requisites

1. A valid set of AWS credentials.

2. Enumerate user accounts with less than 2 access keys:

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

Create a new access key for the svc-mfghwteste-wef102-upload-user IAM user:

```bash
./ttpforge -c config.yaml \
      run ttps/cloud/aws/iam/revive-old-iam-user/revive-old-iam-user.yaml \
      --arg user=mountainpass-budgetchecker \
      --arg cleanup=true \
      --arg detect=false
```

Create a new access key for the mountainpass-file-inject IAM user,
log the results in a custom logfile, and get detection information:

```bash
./ttpforge -c config.yaml \
      -l revive-old-iam-user.log \
      run ttps/cloud/aws/iam/revive-old-iam-user/revive-old-iam-user.yaml \
      --arg user=mountainpass-budgetchecker \
      --arg cleanup=true \
      --arg detect=true
```
