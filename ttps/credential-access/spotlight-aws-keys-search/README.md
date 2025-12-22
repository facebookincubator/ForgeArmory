# Leverage mdfind to search for AWS credentials on disk

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP uses `mdfind` to locate any files containing the string "AKIA". This
string is typically indicative of an AWS access key, suggesting the presence of
potentially sensitive credentials.

## Pre-requisites

1. The user must have the necessary permissions to run `mdfind`.
1. This TTP must be executed on a macOS system.

## Examples

You can run the TTP using the following example:

```bash
ttpforge run forgearmory//credential-access/spotlight-aws-keys-search/ttp.yaml
```

## Steps

1. **mdfind_aws_keys**: This step uses `mdfind` to search for files containing
   the string "AKIA" within the user's home directory.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0006 Credential Access
- **Techniques**:
  - T1552 Unsecured Credentials
- **Sub-techniques**:
  - T1552.001 Unsecured Credentials: Credentials In Files
