# escalate-old-iam-user

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

Add previously dormant IAM user to a privileged group or remove them from that group.

## Arguments

- **user**: Target IAM user.
- **group**: Target IAM group to add to the IAM user.
- **cleanup**: When set to true, remove the IAM user from the group.

## Pre-requisites

1. A valid set of AWS credentials.
1. Create a list of enumerated dormant IAM user accounts:

  ```bash
  #!/bin/bash
  set -e

  usernames=($(aws iam list-users --output json | jq -r '.Users[].UserName'))

  for user in ${usernames[@]}; do
    echo "Reviewing access keys for ${user}:"
    output=$(aws iam list-access-keys --user-name ${user} --output json 2>&1)

    if echo $output | grep -q "cannot be found"; then
      echo "The user ${user} does not exist."
      continue
    fi

    keys=($(echo $output | jq -r '.AccessKeyMetadata[].AccessKeyId'))

    if [ -z "${keys}" ]; then
      echo "${user} has no access keys."
      continue
    fi

    for key in ${keys[@]}; do
      output=$(aws iam get-access-key-last-used --access-key-id ${key} --output json 2>&1)

      if echo $output | grep -q "cannot be found"; then
        echo "The access key ${key} does not exist."
        continue
      fi

      last_used=$(echo $output | jq -r .AccessKeyLastUsed.LastUsedDate)

      if [[ ${last_used} == "null" ]]; then
        echo "${user} has an access key that's never been used!"
      else
        last_used_sec=$(date -j -f "%Y-%m-%dT%H:%M:%S+00:00" "${last_used}" +%s)
        upper_bound_sec=$(date -j -v-90d +%s)

        if [[ ${last_used_sec} -lt ${upper_bound_sec} ]]; then
          echo "${user} has not used access key ${key} in over 90 days!"
        else
          echo "${user} has been used within the last 90 days!"
        fi
      fi
    done
  done
  ```

## Examples

Add `old-and-forgotten` IAM user to the `priv-group` privileged group:

```bash
./ttpforge -c config.yaml \
      run ttps/cloud/aws/iam/escalate-old-iam-user/escalate-old-iam-user.yaml \
      --arg user=old-and-forgotten \
      --arg group=priv-group \
      --arg cleanup=false
```

Remove `old-and-forgotten` IAM user from the `priv-group` privileged group:

```bash
./ttpforge -c config.yaml \
      run ttps/cloud/aws/iam/escalate-old-iam-user/escalate-old-iam-user.yaml \
      --arg user=old-and-forgotten \
      --arg group=priv-group \
      --arg cleanup=true
```

## Steps

1. **Identify Dormant Users**: Using the provided script, scan for users that
   have not used access keys in over 90 days.

2. **Add or Remove from Group**: Depending on the parameters,
   the TTP will either add the identified IAM user to the specified
   privileged group or remove them from the group.

3. **Validate Changes**: Check that the changes have been made as intended
   within the AWS environment.

4. **Cleanup**: If the `cleanup` argument is set to true, the TTP will
   remove the IAM user from the group.
