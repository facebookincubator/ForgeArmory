# Extract Kubernetes Secrets

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP demonstrates how to steal Kubernetes secrets from a target cluster. It
assumes access to a compromised cluster. The TTP retrieves the secrets using the
`kubectl get secrets` command and stores them for later exfiltration.

## Arguments

- **artifacts_dir**: The directory to store the retrieved secrets.

  Default: /tmp

- **eks_cluster**: Indicates if the target Kubernetes cluster is running on EKS.

  Default: true

- **target_cluster**: The name of the target Kubernetes cluster.

- **target_ns**: The namespace from which secrets will be stolen.
  If set to `NIL`, secrets will be retrieved from all namespaces.

  Default: NIL

- **target_region**: The region where the target cluster is located.

  Default: us-east-1

## Requirements

1. Kubernetes cluster with access to run commands and retrieve secrets.
1. `kubectl` installed and configured to interact with the target cluster.

### EKS

1. A valid set of AWS credentials. They can be provided through environment variables:

   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_SESSION_TOKEN`

     OR:

   - `AWS_PROFILE`

1. The AWS CLI is installed.
1. The system should have `python3`, `pip3`, and `git` installed.

## Examples

You can run the TTP using the following command (adjust arguments as needed):

```bash
ttpforge run forgearmory//credential-access/containers/k8s/secrets/extract_k8s_secrets.yaml \
    --arg target_cluster=YOUR-CLUSTER-NAME
```

## Steps

1. **aws_connector**: Validates and sets up the AWS environment (if targeting an
   EKS cluster).
1. **setup_kubeconfig_for_eks**: Sets up kubeconfig for EKS cluster (if targeting
   an EKS cluster).
1. **steal-secrets**: Retrieves Kubernetes secrets from the target namespace (or
   all namespaces if not specified) and saves them as a JSON file.
1. **exfiltrate-secrets**: Outputs the location of the stolen secrets for later
   exfiltration.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0006 Credential Access
- **Techniques**:
  - T1552 Unsecured Credentials
