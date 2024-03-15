# KubeletMeIn: Privilege Escalation in Kubernetes

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP demonstrates how to gain escalated privileges on a Kubernetes node
from an insecure pod. It creates a pod with root access, copies the [kubectl](https://kubernetes.io/docs/reference/kubectl/kubectl/)
and [kubeletmein](https://github.com/4ARMED/kubeletmein) tools to the pod, moves
these tools to the host node, generates Kubernetes credentials using
`kubeletmein`, and uses `kubectl` with the new credentials to interact with the
Kubernetes cluster.

## Arguments

- **artifacts_dir**: The directory to store the downloaded tools.

  Default: /tmp

- **eks_cluster**: Target k8s cluster is running on EKS.

  Default: true

- **insecure_container_image**: The container image to employ for the insecure
  pod.

  Default: ubuntu:latest

- **target_arch**: The architecture the target k8s pod is running.

  Default: amd64

- **target_cluster**: The target k8s cluster.

- **target_ns**: Namespace the insecure pod lives in.

  Default: default

- **target_os**: The operating system the target k8s pod is running.

  Default: linux

- **target_region**: The region the target EKS cluster is in.

  Default: us-east-1

## Requirements

1. Kubernetes cluster with access to create pods and services.
1. `kubectl` installed and configured to interact with the target cluster.

### EKS

1. A valid set of AWS credentials. They can be provided through environment variables:

   - `AWS_ACCESS_KEY_ID`,
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_SESSION_TOKEN`

     OR:

   - `AWS_PROFILE`.

1. The AWS CLI is installed.

1. The system should have `python3`, `pip3`, and `git` installed.

## Examples

You can run the TTP using the following command (adjust arguments as needed):

```bash
ttpforge run forgearmory//privilege-escalation/containers/k8s/pod-escape/kubeletmein/kubeletmein.yaml \
    --arg target_cluster=YOUR-CLUSTER-NAME
```

## Steps

1. **aws_connector**: Invokes the setup_cloud_env action (if EKS cluster).
1. **setup_kubeconfig_for_eks**: Sets up kubeconfig for EKS cluster (if EKS cluster).
1. **download-kubeletmein**: Downloads the latest releases of kubeletmein from
   GitHub.
1. **download-kubectl**: Downloads the latest release of kubectl.
1. **create_insecure_pod_manifest**: Creates the manifest for the insecure pod.
1. **create_insecure_pod**: Creates the insecure pod in the target namespace.
1. **copy-tools-to-insecure-pod**: Copies the downloaded tools to the insecure pod.
1. **move-tools-to-node**: Moves the tools from the insecure pod to the node.
1. **configure-node-and-get-pods**: Configures the node with credentials and
   gets the pods in the target namespace.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0004 Privilege Escalation
  - TA0007 Discovery
- **Techniques**:
  - T1552 Unsecured Credentials
  - T1087 Account Discovery
  - T1082 System Information Discovery
