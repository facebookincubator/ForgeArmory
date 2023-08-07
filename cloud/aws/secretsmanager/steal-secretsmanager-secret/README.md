# steal-secretsmanager-secret

This script uses AWS CLI commands to exfiltrate secrets from AWS Secrets Manager.

## Arguments

- **detect**: If set to true, the script will
  query CloudTrail to determine if the secret
  retrieval was logged.
- **target_secret_id**: The ID of the secret that
  you want to steal. If this is set to "all", the
  script will attempt to steal all secrets.
- **cleanup**: When set to true, the script will
  delete the pillaged secrets after execution.

## Pre-requisites

1. A valid set of AWS credentials. The AWS credentials can be
   provided either as environment variables (`AWS_ACCESS_KEY_ID`,
   `AWS_SECRET_ACCESS_KEY`, and optionally `AWS_SESSION_TOKEN`) or
   via an `AWS_PROFILE`.
1. The AWS CLI is installed.

## Examples

You can run the script using the following examples:

Steal a specific secret, detect if the action was logged, and clean up afterwards:

```bash
ttpforge -c config.yaml run ttps/cloud/aws/secretsmanager/steal-secretsmanager-secret.yaml \
    --arg target_secret_id=ssh_key \
    --arg cleanup=true \
    --arg detect=true
```

Steal all secrets, detect if the action was logged, but do not clean up afterwards:

```bash
ttpforge -c config.yaml run ttps/cloud/aws/secretsmanager/steal-secretsmanager-secret.yaml \
    --arg target_secret_id=all \
    --arg cleanup=false \
    --arg detect=true
```

## Steps

1. **Setup**: This step checks if the necessary tools and environment
   variables are available.

1. **Run enumerate-iam**: This step runs the enumerate-iam script using
   the provided AWS credentials.

1. **Steal Secret:** This step runs the AWS CLI command to retrieve the
   secret or secrets specified by target_secret_id.

1. **Cleanup:** If cleanup is set to true, this step will delete
   the pillaged secrets.

1. **Check Detection:** If detect is set to true, this step will look
   for specific API calls in the CloudTrail logs within a certain time
   window. If it finds specific API calls (GetSecretValue, ListSecrets)
   from the same IP address, it will output the details.
