# Escaper: Pod Escape in Kubernetes

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP demonstrates how to escape from an insecure pod to a node in a
Kubernetes cluster using the [escaper](https://github.com/danielsagi/kube-pod-escape)
tool. The TTP creates an insecure pod with the escaper container image, which has
the capability to mount the host's filesystem. Once the pod is running, it verifies
access to a specified file on the host node to confirm the escape was successful.

## Arguments

- **artifacts_dir**: The directory to store the downloaded tools.

  Default: /tmp

- **eks_cluster**: Target k8s cluster is running on EKS.

  Default: true

- **host_filepath**: The file path on the host to access.

  Default: /var/log/host/cloud-init.log

- **insecure_container_image**: The container image to employ for the insecure pod.

  Default: danielsagi/kube-pod-escape

- **target_cluster**: The target k8s cluster.

- **target_ns**: The target namespace in the cluster.

  Default: default

- **target_region**: The region the target EKS cluster is in (optional).

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
ttpforge run forgearmory//privilege-escalation/k8s-escaper/ttp.yaml \
    --arg target_cluster=YOUR-CLUSTER-NAME
```

## Steps

1. **aws_connector**: Invokes the setup_cloud_env action (if EKS cluster).
1. **setup_kubeconfig_for_eks**: Sets up kubeconfig for EKS cluster (if EKS cluster).
1. **create_insecure_pod_manifest**: Creates the manifest for the insecure pod.
1. **create_insecure_pod**: Creates the insecure pod in the target namespace.
1. **verify_k8s_node_access**: Ensures that we have successfully broken out of
   the pod and can access the k8s node.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0004 Privilege Escalation
  - TA0007 Discovery
- **Techniques**:
  - T1552 Unsecured Credentials
  - T1087 Account Discovery
  - T1082 System Information Discovery
