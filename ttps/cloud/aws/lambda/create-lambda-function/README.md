# Create AWS Lambda Function

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP is used to create a new Lambda function in AWS. It uses the AWS CLI to create a new function with the specified name.
  A temprory IAM role, S3 bucket are created to hold the lambda function code.
  If a function with given name exists, no new function is created.
  If a function does not exist a new function is created. It is also deleted during cleanup.
  A public API gateway is created to also invoke this function. This enables use to invoke the function from the internet.
  `--no-cleanup` options should be explicitly specified if we do not want the new function created to be deleted.


## Arguments

- **region**: Name of the AWS region to use with TTPForge.
- **lambda_function_name**: The name of the new Lambda function to be created.

## Steps

1. Set up necessary cloud environment variables.
2. Create a temprory IAM role to be assumed by the lambda function.
3. Create a S3 bucket with a random string name
4. Zip and upload lambad code from local device to the newly created S3 bucket.
5. Create a new Lambda function if no existing function is found with given function name.
6. Create a API which is publicly accessible and integrate the newly created lambda function with it.
6. Invoke the newly created Lambda function by accessing the API URL
7. By default during the cleanup, delete the recently created Lambda function, S3 bucket, IAM role and the API gateway.

## Manual Reproduction Steps

```
# Set necessary env variables

# Create new temp IAM role
aws iam create-role --role-name "ROLE-NAME" --assume-role-policy-document file://trust-policy.json

# Create a new S3 bucket to host lambda function
aws s3 mb s3://BUCKET_NAME

# Upload lambda function zip file to S3 bucket
aws s3 cp lambda-function.zip s3://BUCKET_NAME

# Create a new function
aws lambda create-function --function-name "FUNCTION_NAME" --runtime "RUNTIME" --handler "HANDLER" --role "ROLE_ARN" --code "S3Bucket=$BUCKET_NAME,S3Key=lambda-function.zip"

# Create a new REST API
rest_api_id=$(aws apigateway create-rest-api --name "FUNCTION_NAME"-api --query 'id' --output text)

# Get the root resource id
root_resource_id=$(aws apigateway get-resources --rest-api-id $rest_api_id --query 'items[?path==`/`].id' --output text)

# Create a GET method for the new resource
aws apigateway put-method --rest-api-id $rest_api_id --resource-id $root_resource_id --http-method GET --authorization-type "NONE" > /dev/null 2>&1

# Add necessary permissions to the new resource method
lambda_func_arn=$(aws lambda get-function --function-name "FUNCTION_NAME" --query 'Configuration.FunctionArn' --output text)
account_id=$(aws sts get-caller-identity --query Account --output text)
account_region=$(aws configure get region)
source_arn="arn:aws:execute-api:$account_region:$account_id:$rest_api_id/*/*/"

aws lambda add-permission --function-name $lambda_func_arn --source-arn $source_arn --principal apigateway.amazonaws.com --statement-id apigateway-test1-"FUNCTION_NAME" --action lambda:InvokeFunction > /dev/null 2>&1


# Connect the GET method to the Lambda function (define integration)
lambda_invocation_uri="arn:aws:apigateway:$account_region:lambda:path/2015-03-31/functions/$lambda_func_arn/invocations"
aws apigateway put-integration --rest-api-id $rest_api_id --resource-id $root_resource_id --http-method GET --type AWS --integration-http-method POST --uri $lambda_invocation_uri > /dev/null 2>&1


# Specify an INTEGRATION RESPONSE for a method response code of 200 and allow Passthrough content handling
aws apigateway put-integration-response --rest-api-id $rest_api_id --resource-id $root_resource_id --http-method GET --status-code 200 > /dev/null 2>&1

# Specify a METHOD response for HTTP status code 200
aws apigateway put-method-response --rest-api-id $rest_api_id --resource-id $root_resource_id --http-method GET --status-code 200 > /dev/null 2>&1

# Deploy the API
aws apigateway create-deployment --rest-api-id $rest_api_id --stage-name prod  > /dev/null 2>&1

# Get the invoke URL and curl it
invoke_url="https://$rest_api_id.execute-api.$account_region.amazonaws.com/prod"
curl $invoke_url

```

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1098 Account Manipulation
