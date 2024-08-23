# Backdoor Kubernetes Nodes with Authorized Keys

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP adds a rogue public SSH key to the `authorized_keys` file on all Kubernetes
nodes to maintain persistence. It assumes access to a Kubernetes cluster with the
ability to execute commands on the nodes. The TTP makes a backup of the original
`authorized_keys` file before overwriting it and restores it during cleanup.

## Arguments

- **artifacts_dir**: The directory to store the downloaded tools.

  Default: /tmp

- **eks_cluster**: Indicates if the target Kubernetes cluster is running on EKS.

  Default: true

- **rogue_key**: The rogue public SSH key to be added to the `authorized_keys` file.

- **ssh_authorized_keys**: Path to the `authorized_keys` file.

  Default: `$HOME/.ssh/authorized_keys`

- **target_cluster**: The name of the target Kubernetes cluster.

- **target_ns**: The namespace for deploying the privileged pod.

  Default: kube-system

- **target_region**: The region where the target cluster is located.

  Default: us-east-1

## Requirements

1. Kubernetes cluster with access to run privileged commands and modify files on
  the nodes.
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
ttpforge run forgearmory//persistence/containers/k8s/backdoor-k8s-nodes-authorized-keys/backdoor-k8s-nodes-authorized-keys.yaml \
    --arg rogue_key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGXY7PWSZ7QafZ5LsBxGVtAcAwn706dJENP1jXlX3fVa Test public key" \
    --arg target_cluster=YOUR-CLUSTER-NAME
```

## Steps

1. **aws_connector**: Validates and sets up the AWS environment (if targeting an
   EKS cluster).
1. **setup_kubeconfig_for_eks**: Sets up kubeconfig for EKS cluster (if targeting an
   EKS cluster).
1. **create_privileged_pod_manifest**: Creates a privileged pod manifest for executing
   commands on the nodes.
1. **deploy_privileged_pod**: Deploys the privileged pod in the target namespace.
1. **modify_authorized_keys_on_nodes**: Backs up and modifies the `authorized_keys`
   file on all Kubernetes nodes, adding the rogue SSH key.
1. **cleanup**: Restores the original `authorized_keys` files and deletes the
   privileged pod.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1078 Valid Accounts
