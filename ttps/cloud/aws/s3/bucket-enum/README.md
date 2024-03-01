# s3-bucket-enum

Enumerate open S3 buckets using the
[S3Scanner](https://github.com/sa7mon/S3Scanner) tool.

## Arguments

- **bucket_list**: File path to store the list of bucket names.
- **create_bucket_list**: When set to true, attempt to create a list of buckets
  found in the specified region.
- **detect**: When set to true, query CloudTrail to determine if the TTP was logged.
- **region**: AWS region to search for S3 buckets.
- **concurrent_processes**: Number of concurrent processes to use for scanning.

## Requirements

1. A valid set of AWS credentials. They can be provided through environment variables:

   - `AWS_ACCESS_KEY_ID`,
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_SESSION_TOKEN`

     OR:

   - `AWS_PROFILE`.

1. The AWS CLI is installed.

1. The system should have `python3`, `pip3`, and `git` installed.

## Examples

Populate a list of buckets, install required tooling, and run the TTP:

```bash
ttpforge run forgearmory//cloud/aws/s3/bucket-enum/bucket-enum.yaml \
    --arg bucket_list=/tmp/buckets.txt \
    --arg create_bucket_list=true
```

Run the TTP using a wordlist from the [SecLists repo](https://github.com/danielmiessler/SecLists):

```bash
ttpforge run forgearmory//cloud/aws/s3/bucket-enum/bucket-enum.yaml \
    --arg bucket_list=/data/users/jaysong/fbsource/fbcode/security/redteam/purple_team/ForgeArmory/SecLists/Usernames/top-usernames-shortlist.txt \
    --arg create_bucket_list=false
```

## Steps

1. **AWS Connector**: This step validates the necessary AWS credentials and region settings for the TTP.

1. **Create Bucket List**: If `create_bucket_list` is set to `true`, this
   step will create a file specified by the `bucket_list` argument and populate
   it with the names of S3 buckets associated with the currently configured AWS
   credentials. Only buckets located in the region specified by the `region`
   argument will be included.

1. **Provision**: This step installs the necessary tools for bucket enumeration,
   specifically the S3Scanner tool.

1. **Bucket Discovery**: This step discovers S3 buckets using the S3Scanner tool.

1. **Check Detection**: If `detect` is set to `true`, this
   step will look for
   specific API calls in the CloudTrail logs within a certain time window. If
   it finds more than a threshold number of calls from the same IP address, it
   will raise an alert.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0009 Collection
- **Techniques**:
  - T1530 Data from Cloud Storage Object
- **Subtechniques**:
  - T1530.001 Cloud Storage API
