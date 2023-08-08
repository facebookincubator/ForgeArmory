# enumerate-iam

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This script uses the [enumerate-iam](https://github.com/andresriancho/enumerate-iam)
tool to determine what permissions an IAM role has through brute force.

## Arguments

- **detect**: If set to true, the script will query CloudTrail to determine if the IAM enumeration was logged.
- **eiam_path**: Specifies the location to clone and manage the enumerate-iam tool.
- **extended_scan**: When set to true, the script will use the
  extended AWS APIs to enumerate permissions.
  Note that this will take longer but will provide more accurate results.
- **cleanup**: When set to true, the script will uninstall the
  Python packages and clean up the enumerate-iam repository
  after execution.

## Pre-requisites

1. A valid set of AWS credentials. The AWS credentials can be
   provided either as environment variables (`AWS_ACCESS_KEY_ID`,
   `AWS_SECRET_ACCESS_KEY`, and optionally `AWS_SESSION_TOKEN`) or
   via an `AWS_PROFILE`.
1. The system should have Python3, pip3, and git installed.
1. If enumerate-iam is not installed, the project will be cloned from
   its GitHub repository.

## Examples

You can run the script using the following examples:

Execute the `enumerate-iam` tool at a specified path. Post execution,
it cleans up the artifacts:

```bash
ttpforge -c config.yaml run ttps/cloud/aws/iam/enumerate-iam/enumerate-iam.yaml \
    --arg detect=true \
    --arg eiam_path=/tmp/enumerate-iam \
    --arg extended_scan=false \
    --arg cleanup=true
```

Run the `enumerate-iam` tool with extended APIs at a specified path,
skip the cleanup step, log results to a custom file, and get detection
data. This will take more time due to the use of extended APIs:

```bash
ttpforge -c config.yaml run ttps/cloud/aws/iam/enumerate-iam/enumerate-iam.yaml \
    -l brute-force-iam-permissions.log \
    --arg detect=true \
    --arg eiam_path=/tmp/enumerate-iam \
    --arg extended_scan=true \
    --arg cleanup=false
```

## Steps

1. **Setup**: This step checks if the necessary tools and environment
   variables are available. It also checks if the enumerate-iam tool is
   already present on the system; if not, it will clone the tool from
   GitHub. If `extended_scan` is set to true, the script will clone the
   latest AWS API endpoints.

1. **Run enumerate-iam**: This step runs the enumerate-iam script using
   the provided AWS credentials.

1. **Cleanup**: If `cleanup` is set to true, this step will uninstall
   the Python packages required by the enumerate-iam tool and clean up the cloned repository.

1. **Check Detection**: If `detect` is set to true, this step will look
   for specific API calls in the CloudTrail logs within a certain time
   window. If it finds more than a threshold number of calls from the same IP address, it will raise an alert.
