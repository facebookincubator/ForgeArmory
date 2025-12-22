# ForgeArmory

[![License](https://img.shields.io/github/license/facebookincubator/ForgeArmory?label=License&style=flat&color=blue&logo=github)](https://github.com/facebookincubator/ForgeArmory/blob/main/LICENSE)
[![🚨 Semgrep Analysis](https://github.com/facebookincubator/ForgeArmory/actions/workflows/semgrep.yaml/badge.svg)](https://github.com/facebookincubator/ForgeArmory/actions/workflows/semgrep.yaml)
[![Pre-Commit](https://github.com/facebookincubator/ForgeArmory/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/facebookincubator/ForgeArmory/actions/workflows/pre-commit.yaml)

ForgeArmory is a repository of attacker Tactics, Techniques, and Procedures
(TTPs) that you can download and run with Meta's
[TTPForge](https://github.com/facebookincubator/TTPForge) attack simulation
engine. Our catalog presently focuses on macOS and Cloud TTPs.

## Setup

To get started,
[install TTPForge](https://github.com/facebookincubator/TTPForge/blob/main/README.md#installation)
and then browse the ForgeArmory
[TTP catalog](https://github.com/facebookincubator/ForgeArmory/tree/main/ttps)
to find cyberattacks to simulate.

## Repository Structure

ForgeArmory TTPs are organized by
[MITRE ATT&CK](https://attack.mitre.org/) tactics, making it easy to
find and execute specific attack techniques.

Each TTP is contained in its own directory with a standardized
structure:

```
ttps/<MITRE-TACTIC>/<TTP-NAME>/
├── ttp.yaml          # TTP definition and execution logic
├── README.md         # Documentation and usage instructions
└── [helper files]    # Supporting scripts, binaries, or resources
```

### Preferred Naming Convention

TTPs should be named according to the action they perform, independent
of the platform or operating system they target.

For ease of identification, however, names should be prefixed with the technology
they target:

Cloud-based TTPs are prefixed with the cloud service:

- **AWS EC2**: `aws-ec2-*` (instance management, exfiltration)
- **AWS IAM**: `aws-iam-*` (user/role manipulation, persistence)
- **AWS Lambda**: `aws-lambda-*` (serverless backdoors)
- **AWS S3**: `aws-s3-*` (bucket enumeration)
- **AWS Secrets Manager**: `aws-secretsmanager-*` (secret extraction)

Similarly, Kubernetes and container-based TTPs are prefixed with
`k8s-`:

- `k8s-extract-k8s-secrets` - Extract secrets from Kubernetes clusters
- `k8s-backdoor-k8s-nodes-authorized-keys` - Backdoor cluster nodes
- `k8s-escaper` - Container escape techniques
- `k8s-kubeletmein` - Kubelet exploitation

### Utilities and Chains

Helper TTPs for use in subTTPs are located in `ttps/utils/`. Examples include:

- **AWS utilities**: Environment validation and credential management
- **Kubernetes utilities**: Cluster configuration and validation

Complex TTPs that span multiple MITRE tactics can be stored in `ttps/chains`.

### Browsing and Filtering TTPs

You can use the [`ttpforge enum`](https://github.com/facebookincubator/TTPForge/blob/main/docs/foundations/enum.md) command to list and filter TTPs by various criteria:

```bash
# List all available TTPs
ttpforge enum ttps -v

# Filter by MITRE technique
ttpforge enum ttps --technique T1552 -v

# Filter by MITRE subtechnique
ttpforge enum ttps --sub-tech T1552.001 -v

# Filter by operating system
ttpforge enum ttps --platform <platform> -v

# Filter by author
ttpforge enum ttps --author <author-name> -v
```

For complete documentation on filtering and enumeration options with enum, see
the official [TTPForge documentation](https://github.com/facebookincubator/TTPForge/blob/main/docs/foundations/enum.md).

## Adding New TTPs

You can add new TTPs to ForgeArmory by [forking](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
this repository and adding your TTP YAML files to the appropriate
directories in the [catalog](https://github.com/facebookincubator/ForgeArmory/tree/main/ttps).
Check out the [TTPForge documentation](https://github.com/facebookincubator/TTPForge/blob/main/docs/foundations/README.md)
to learn the syntax for writing TTPs and all of TTPForge's attack
simulation features.

## Submitting Pull Requests

Once your TTPs are ready, feel free to send us a pull request :)

Our automation will run various linters and checks against new pull
requests. Several of the linters in this project may be used as
pre-commit hooks if desired - you can install and setup pre-commit
according to the [official instructions](https://pre-commit.com/).

For quick ad hoc runs, you may wish to run pre-commit in a virtual
environment:

```bash
python3 -m venv venv
. venv/bin/activate
pip3 install pre-commit
pre-commit run --all-files
```
