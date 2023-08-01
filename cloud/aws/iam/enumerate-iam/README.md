# brute-force-iam-permissions

Determine what permissions an IAM role has through brute force
using the [enumerate-iam](https://github.com/andresriancho/enumerate-iam) tool.

## Arguments

- detect: When set to true, query cloudtrail to determine if the
  TTP was logged.

- extended-scan: When set to true, use the extended APIs to
  enumerate permissions. This will take longer, but will provide
  more accurate results.

## Pre-requisites

A valid set of AWS credentials.

## Examples

Install and execute the `enumerate-iam` tool and get detection
information:

```bash
./ttpforge -c config.yaml run ttps/cloud/aws/iam/enumerate-iam/enumerate-iam.yaml \
    --arg detect=true \
    --arg eiam_path=/tmp/enumerate-iam \
    --arg extended_scan=false
```

Run the TTP using the extended APIs (TTP will take longer), log the
results in a custom logfile, and get detection information using an
existing bucket inputs file:

```bash
./ttpforge -c config.yaml run ttps/cloud/aws/iam/enumerate-iam/enumerate-iam.yaml \
    -l brute-force-iam-permissions.log \
    --arg detect=true \
    --arg eiam_path=/tmp/enumerate-iam \
    --arg extended_scan=true
```
