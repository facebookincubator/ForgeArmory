import os


def lambda_handler(event, context):
    data = os.popen("printenv").read()
    data_list = data.split("\n")
    formatted_data = "\n".join(data_list)
    return {
        "statusCode": 200,
        "body": formatted_data,
        "headers": {
            "Content-Type": "text/plain",
        },
        "isBase64Encoded": False,
    }
