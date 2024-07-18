# Create new IAM user

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP is used to create a new IAM user in AWS. It uses the AWS CLI to create a new user with the specified name.
  If a user with given name exists, nothing is done and the TTP is closed.
  If a user does not exist a new user is created.
  It is also deleted during cleanup. `--no-cleanup` options should be explicity specified if we do not want the new user created to be deleted.


## Arguments


- **iam_user_name**: The name of the new IAM user to be created.

## Steps

1. Set up necessary cloud environment variables.
2. Check if an IAM user exists with provided user name
3. Create a new IAM user if no existing user is found with given IAM user name.
4. By deafult during the cleanup, delete the recently created IAM user.

## Manual Reproduction Steps

```

# Check if a user exists with provided user name
aws iam get-user --user-name "IAM_USER_NAME"

# Create a new user
aws iam create-user --user-name "IAM_USER_NAME"

# Setup persistence command in a RC SHELL script file: eg
aws iam delete-user --user-name "IAM_USER_NAME"

```

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1098 Account Manipulation
