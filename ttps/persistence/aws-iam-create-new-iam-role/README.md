# AWS IAM Role Creation for Persistence

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP creates a new IAM role in AWS with a malicious trust policy
that allows an attacker-controlled AWS account to assume the role. This
technique can be used for persistence by establishing a backdoor access
mechanism in the victim's AWS environment.

## Arguments

- **iam_role_name**: The name of the new IAM role to be created
  (default: `ttpforge_trojan_role`)
- **attacker_account_id**: The attacker's AWS account ID that will be
  granted permission to assume the newly created role

## Prerequisites

1. Valid AWS credentials must be configured (via environment variables
   or AWS CLI configuration)
2. The AWS CLI must be installed
3. Sufficient IAM permissions to create roles and attach trust policies

## Examples

Create a backdoored IAM role (will be cleaned up automatically):

```bash
ttpforge run forgearmory//persistence/aws-iam-create-new-iam-role/ttp.yaml \
    --arg attacker_account_id=123456789012
```

Create a backdoored IAM role with custom name:

```bash
ttpforge run forgearmory//persistence/aws-iam-create-new-iam-role/ttp.yaml \
    --arg iam_role_name=my-backdoor-role \
    --arg attacker_account_id=123456789012
```

Create a backdoored IAM role without automatic cleanup:

```bash
ttpforge run forgearmory//persistence/aws-iam-create-new-iam-role/ttp.yaml \
    --arg attacker_account_id=123456789012 \
    --no-cleanup
```

## Steps

1. **aws-connector**: Validates that AWS credentials are configured and
   the AWS CLI is available
2. **create-policy-file**: Creates a malicious trust policy document
   that allows the attacker's AWS account to assume the role
3. **create_new_role**: Creates the new IAM role with the backdoored
   trust policy attached
   - Cleanup: Deletes the newly created role (unless `--no-cleanup` is
     specified)

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1098 Account Manipulation
- **Subtechniques**:
  - T1098.001 Additional Cloud Credentials
