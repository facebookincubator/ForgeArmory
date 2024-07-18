# Create new IAM role

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

  This TTP is used to create a new IAM role in AWS. It uses the AWS CLI to create a new role with the specified name.
  If a role with given name exists, nothing is done and the TTP is closed.
  If a role does not exist a new role is created. It is also deleted during cleanup.
  A malicious trust policy is also attached to this role that provides an attacker AWS account to assume this role.
  `--no-cleanup` options should be explicity specified if we do not want the new role created to be deleted.

  After a backdoored role has been created, this backdoored role is also accessed from an attacker controlled account to verify that,
  the implemented malicious policy works as intended.


## Arguments
### (Create-new-iam-role)
  - **iam_role_name**: The name of the new IAM role to be created.
  - **attacker_account_id**: Attacker AWS account ID which has been provisioned to access backdoored IAM role.

### (access-iam-role)
  - **iam_role_name**: The name of the  backdoored IAM role to be assumed.
  - **backdoor_account_id**: Backdoor AWS account ID which has been provisioned to access backdoored IAM role.

## Steps

1. Set up necessary cloud environment variables.
2. Check if an IAM role exists with provided role name, exit if found.
3. Create a new IAM role with provided name.
5. Attach a malicious policy that gives external AWS account the ability to assume the role
4. By deafult during the cleanup, delete the recently created IAM role.

5. Verify the caller identity of attacker account
6. Assume the identity of victim using the backdoored role account
7. Verify the identity of assumed role.

## Manual Reproduction Steps

```
# Check if a user exists with provided user name
aws iam get-role --role-name "IAM_ROLE_NAME"

# Create a new user
aws iam create-role --role-name "IAM_ROLE_NAME" --assume-role-policy-document file://backdoor-trust-policy.json

# Assume backdoored role
aws sts assume-role --role-arn "arn:aws:iam::"BACKDOOR_ACCNT_ID":role/"IAM_ROLE_NAME"" --role-session-name "TTPforge_backdoor_role_sessioin"
```

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1098 Account Manipulation
