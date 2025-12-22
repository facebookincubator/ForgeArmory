# enumerate-iam

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP uses the [enumerate-iam](https://github.com/andresriancho/enumerate-iam)
tool to determine what permissions an IAM role has through brute force.

## Arguments

- **detect**: If set to true, the TTP will
  query CloudTrail to determine if the IAM enumeration was logged.

  Default: true

- **eiam_path**: Specifies the location to clone and manage the enumerate-iam
  tool.

  Default: /tmp/enumerate-iam

- **extended_scan**: When set to true, the TTP will use the
  extended AWS APIs to enumerate permissions.
  Note that this will take longer but should provide more accurate results.

  Default: false

## Requirements

1. A valid set of AWS credentials. They can be provided through environment variables:

   - `AWS_ACCESS_KEY_ID`,
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_SESSION_TOKEN`

     OR:

   - `AWS_PROFILE`.

1. The AWS CLI is installed.

1. The system should have `python3`, `pip3`, and `git`
   installed.

1. If `enumerate-iam` is not installed, the project is
   cloned and configured for this TTP. Assuming
   cleanup is run, the TTP will clean up after itself.

## Examples

You can run the TTP using the following examples:

Download, install, and run the `enumerate-iam` tool. Post
execution, it cleans up the artifacts:

```bash
ttpforge run forgearmory//discovery/aws-iam-enumerate-iam/ttp.yaml
```

Download, install, and run the `enumerate-iam` tool with extended APIs.
Post execution, it will skip the cleanup step, and subsequently
artifacts from the TTP will remain on disk.

Note that this will take more time due to the use of extended APIs:

```bash
ttpforge run forgearmory//discovery/aws-iam-enumerate-iam/ttp.yaml \
  --arg extended_scan=true
```

## Steps

1. **Setup**: This step checks if the necessary tools and environment
   variables are available. It also checks if the enumerate-iam tool is
   already present on the system; if not, it will clone the tool from
   GitHub. If `extended_scan` is set to true, the TTP will clone the
   latest AWS API endpoints.

1. **Run enumerate-iam**: This step runs the enumerate-iam script using
   the provided AWS credentials. Unless `--no-cleanup` is specified,
   the cleanup step will uninstall the Python packages required by the
   `enumerate-iam` tool and clean up the cloned repository.

1. **Check Detection**: If `detect` is set to true, this step will look
   for specific API calls in the CloudTrail logs within a certain time
   window. If it finds more than a threshold number of calls from the same IP
   address, it will raise an alert.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0007 Discovery
- **Techniques**:
  - T1082 System Information Discovery
