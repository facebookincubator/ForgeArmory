# Access VNC with Poor Password

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP demonstrates how an attacker can access a VNC server with a poor password
in a Kubernetes cluster. The TTP deploys a headless VNC server in the cluster
and then attempts to access it using a known weak password.

## Arguments

- **artifacts_dir**: The directory to store the downloaded tools.

  Default: /tmp

- **eks_cluster**: Target k8s cluster is running on EKS.

  Default: true

- **target_cluster**: The target k8s cluster.

- **target_ns**: The target namespace in the cluster.

  Default: default

- **target_region**: The region the target EKS cluster is in (optional).

  Default: us-east-1

- **vnc_image**: The container image to use for the VNC server.

  Default: consol/rocky-xfce-vnc

- **vnc_password**: The weak password to use for accessing the VNC server.

  Default: vncpassword

- **vnc_port**: The port on which the VNC server is exposed.

  Default: 5901

- **vnc_server**: The hostname or IP address of the VNC server.

  Default: localhost

- **vnc_username**: The username to use for accessing the VNC server.

  Default: root

## Requirements

1. Kubernetes cluster with access to create pods and services.
1. `kubectl` installed and configured to interact with the target cluster.
1. VNC client installed on the local machine (e.g., VNC Viewer).

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
ttpforge run forgearmory//execution/containers/k8s/vnc/access-vnc-with-poor-password/access-vnc-with-poor-password.yaml \
    --arg target_cluster=YOUR-CLUSTER-NAME
```

## Steps

1. **aws_connector**: Invokes the setup_cloud_env action (if target is an EKS cluster).
1. **setup_kubeconfig_for_eks**: Sets up kubeconfig for EKS cluster (if
   target is an EKS cluster).
1. **deploy_headless_vnc**: Deploys a headless VNC server in the Kubernetes cluster.
1. **wait_for_pod_ready**: Waits for the VNC pod to be ready.
1. **access_vnc_server**: Attempts to access the VNC server using the weak password.

## MITRE ATT&CK Mapping

- **Tactics**:

  - TA0004 Privilege Escalation
  - TA0007 Discovery

- **Techniques**:
  - T1552 Unsecured Credentials
  - T1087 Account Discovery
