# brute-force-iam-permissions

Attempt to identify the permissions tied to compromised credentials.

Once an attacker has compromised a credential, they will want to
understand the scope of access. To do this, they will commonly
employ a bruteforce strategy against the various AWS APIs.

## Arguments

- detect: When set to true, query cloudtrail to determine if the
  TTP was logged.

- provision: When set to true, attempt to install the tooling required
  to run this TTP.

- extended-scan: When set to true, use the extended APIs to
  enumerate permissions. This will take longer, but will provide
  more accurate results.

## Pre-requisites

A valid set of AWS credentials.

## Examples

Install and execute the `enumerate-iam` tool and get detection
information:

```bash
./ttpforge -c config.yaml \
    run ttps/cloud/aws/iam/brute-force-iam-permissions/brute-force-iam-permissions.yaml \
    --arg provision=true \
    --arg detect=true \
    --arg extended-scan=false
```

Run the TTP using the extended APIs (TTP will take longer), log the
results in a custom logfile, and get detection information using an
existing bucket inputs file:

```bash
./ttpforge \
    -c config.yaml \
    -l brute-force-iam-permissions.log \
    run ttps/cloud/aws/iam/brute-force-iam-permissions/brute-force-iam-permissions.yaml \
    --arg provision=true \
    --arg detect=true \
    --arg extended-scan=true
```
