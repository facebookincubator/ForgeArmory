# Sample GuardDuty finding

## Description
This TTP creates a sample AWS GuardDuty finding for e2e testing purposes. The generated finding should be processed by security pipelines to validate detection and alerting workflows.

## Arguments
- **region**: AWS region to create the finding in. Defaults to `us-west-1`.
- **detector_id**: GuardDuty detector ID to use. Defaults to `CHANGEME`.
- **finding_type**: The type of GuardDuty finding to create. Defaults to `Stealth:S3/ServerAccessLoggingDisabled`.

## Requirements
1. Linux platform.
2. AWS CLI installed and configured with credentials that have GuardDuty permissions.
3. An active GuardDuty detector in the target region.

## Examples
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/aws-guardduty-create-sample-finding/ttp.yaml
```

With a custom finding type:
```bash
ttpforge run forgearmory//defense-evasion/aws-guardduty-create-sample-finding/ttp.yaml \
  --arg finding_type=UnauthorizedAccess:EC2/MaliciousIPCaller.Custom
```

## Steps
1. **Create Sample Guard Duty Finding**: Creates a sample GuardDuty finding using the AWS CLI. This action cannot be undone, so there is no cleanup step.
