# steal-secretsmanager-secret

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP uses AWS CLI commands to exfiltrate secrets from AWS Secrets Manager.

## Arguments

- **detect**: If set to true, the TTP will query CloudTrail to determine
  if the secret retrieval was logged.

  Default: true

- **target_secret_id**: Specifies the ID of the target secret in Secrets
  Manager. If set to `all`, it will retrieve all secrets accessible within
  the specified AWS region (provided by setting `$AWS_DEFAULT_REGION`).

- **artifact_output_dir**: The directory where the stolen secrets will be
  stored.

  Default: `$HOME/.ttpforge/artifacts/steal-secretsmanager-secret`

## Pre-requisites

1. A valid set of AWS credentials. They can be provided through environment
   variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`,
   `AWS_SESSION_TOKEN`, or `AWS_PROFILE`.

1. The AWS CLI is installed.

## Examples

Retrieve a specific secret from Secrets Manager:

```bash
ttpforge run forgearmory//collection/aws-secretsmanager-steal-secretsmanager-secret/ttp.yaml \
    --arg target_secret_id="my-secret-id"
```

Retrieve all secrets from Secrets Manager and do not
clean up the output files:

```bash
ttpforge run forgearmory//collection/aws-secretsmanager-steal-secretsmanager-secret/ttp.yaml \
    --arg target_secret_id=all \
    --no-cleanup
```

## Steps

1. **Setup**: Checks if the AWS credentials are set and if the AWS CLI
   tool is present.

1. **Steal Secret**: If `target_secret_id` is set to `all`, it retrieves
   all secrets accessible in Secrets Manager for the specified region. If a
   specific secret ID is provided, it retrieves only that secret. The
   stolen secrets are stored in the directory specified by
   `artifact_output_dir`. Unless `--no-cleanup` is set, all of the
   retrieved information is deleted.

1. **Check Detection:** If `detect` is set to `true`, this step will look
   for specific API calls in the CloudTrail logs within a certain time
   window. If it finds specific API calls (GetSecretValue, ListSecrets)
   from the same IP address, it will output the details.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0009 Collection
- **Techniques**:
  - T1213 Data from Information Repositories
