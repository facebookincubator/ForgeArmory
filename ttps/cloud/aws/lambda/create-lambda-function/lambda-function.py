import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    sts = boto3.client("sts")
    sts_response = sts.get_caller_identity()
    print("STS Response: ", sts_response)

    logger.info(f"CloudWatch logs group: {context.log_group_name}")

    formatted_sts_response = json.dumps(sts_response, indent=4)
    return {
        "statusCode": 200,
        "body": formatted_sts_response,
        "headers": {
            "Content-Type": "text/plain",
        },
        "isBase64Encoded": False,
    }
