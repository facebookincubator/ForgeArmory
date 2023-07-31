#!/bin/bash
set -e

# Get Instances to Terminate
# Fetches the ID of the EC2 instances to terminate based on a specified tag value.
#
# Usage:
#   get_instances_to_terminate
#
# Output:
#   Outputs the ID of the EC2 instances that have the tag "Name" with value "pt-ttp-steal-creds".
#
# Example(s):
#   INSTANCES=$(get_instances_to_terminate)
get_instances_to_terminate()
                             {
    INSTANCE_NAME_TAG=pt-ttp-steal-creds
    # shellcheck disable=SC2016
    aws ec2 describe-instances \
        --query 'Reservations[].Instances[?Tags[?Key==`Name` && Value==`'$INSTANCE_NAME_TAG'`]].InstanceId' \
        --output text
}

# Terminate Instance
# Terminates a specified EC2 instance.
#
# Usage:
#   terminate_instance [instance_id]
#
# Output:
#   Terminates the instance if it's running. If it's already being terminated, the function skips it.
#   If the instance is in an unexpected state, it throws an error.
#
# Example(s):
#   terminate_instance "i-0abcd1234efgh5678"
terminate_instance()
                     {
    local instance_id=$1
    while true; do
        instance_status=$(aws ec2 describe-instances --instance-ids "$instance_id" \
            --query 'Reservations[0].Instances[0].State.Name' --output text --no-cli-pager)
        if [ "$instance_status" == "terminated" ] || [ "$instance_status" == "shutting-down" ]; then
            echo "Skipping instance $instance_id which is already $instance_status"
            break
        elif [ "$instance_status" == "running" ]; then
            echo "Terminating instance: $instance_id"
            aws ec2 terminate-instances --instance-ids "$instance_id" --no-cli-pager
            break
        else
            echo "Unexpected instance status: $instance_status"
            exit 1
        fi
    done
}

# Delete Security Group
# Deletes a specified security group.
#
# Usage:
#   delete_security_group
#
# Output:
#   Deletes the specified security group if it exists. If it doesn't exist,
#   the function outputs a message indicating so.
#   If the function fails to delete the security group, it retries every
#   5 seconds until successful.
#
# Example(s):
#   delete_security_group
delete_security_group()
                        {
    SEC_GRP=pt-ssm-security-group
    # Attempt to get the ID of the security group and capture any error message
    if SEC_GRP_ID=$(aws ec2 describe-security-groups --group-names "$SEC_GRP" --query 'SecurityGroups[0].GroupId' --output text 2> /dev/null); then
        while true; do
            # Try to delete the security group
            if aws ec2 delete-security-group --group-id="$SEC_GRP_ID" > /dev/null 2>&1; then
                # If successful, exit the loop
                echo "Successfully deleted security group: $SEC_GRP"
                break
            else
                # If unsuccessful, sleep for 5 seconds and try again
                echo "Failed to delete security group: $SEC_GRP. Retrying in 5 seconds..."
                sleep 5
            fi
        done
    else
        echo "Security group $SEC_GRP does not exist, nothing to delete."
    fi
}

instances_to_terminate=$(get_instances_to_terminate)

if [ -z "$instances_to_terminate" ]; then
    echo "No instances to terminate."
else
    IFS=$'\n' # set field separator to newline
    for instance_id in $instances_to_terminate; do
        # Skip empty lines
        if [ -z "$instance_id" ]; then
            continue
        fi
        terminate_instance "$instance_id"
    done
fi

delete_security_group
