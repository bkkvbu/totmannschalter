import json
import os
import time

# import requests
import boto3 as boto3

client = boto3.client('dynamodb')


def update_item(id: str, ttl: str, insert_if_not_exists: bool):
    return client.update_item(
        TableName=os.environ["TABLE_NAME"],
        Key={"id": {
            "S": id
        }},
        UpdateExpression="SET timetolive = :ttl",
        ExpressionAttributeValues={
            ":ttl": {
                "N": ttl
            }
        })


def lambda_handler(event, context):
    slack_path = event["pathParameters"]["slack_path"]
    # TODO validate slack_path
    print(f"Got slack_path: {slack_path}")

    ttl_minutes = 5
    ttl = str(int(time.time() + ttl_minutes * 60))
    print(f"Calculated timestamp: {ttl}")

    response = update_item(slack_path, ttl, False)

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
            'slack_path': 'foo/bar'
        }
    }, None)
