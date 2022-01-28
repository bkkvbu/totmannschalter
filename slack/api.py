import json
import os
import time

# import requests
import boto3 as boto3
from botocore.exceptions import ClientError

from slack.notification import notify, newuser_notification

client = boto3.client('dynamodb')


def update_item(id: str, ttl: str, insert_if_not_exists: bool):
    args = {
        'TableName': os.environ["TABLE_NAME"],
        'Key': {"id": {"S": id
                       }},
        'UpdateExpression': "SET timetolive = :ttl",
        'ExpressionAttributeValues': {
            ":ttl": {
                "N": ttl
            }
        }
    }
    if not insert_if_not_exists:
        args['ConditionExpression'] = "attribute_exists(id)"
    return client.update_item(**args)


def lambda_handler(event, context):
    slack_path = event["pathParameters"]["slack_path"]
    # TODO validate slack_path
    print(f"Got slack_path: {slack_path}")

    ttl_minutes = 5
    ttl = str(int(time.time() + ttl_minutes * 60))
    print(f"Calculated timestamp: {ttl}")

    try:
        response = update_item(slack_path, ttl, False)
    except ClientError as err:
        print(err.operation_name)
        if err.response['Error']['Code'] == 'ConditionalCheckFailedException':
            response = update_item(slack_path, ttl, True)
            notify(slack_path, newuser_notification)
    print(f"Updated item in DynamoDB: {json.dumps(response)}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Updated entry",
        }),
    }


if __name__ == '__main__':
    lambda_handler({
        'pathParameters': {
            'slack_path': 'TB7TK18DD/B03074WD8P'
        }
    }, None)
