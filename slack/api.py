import json
import os
import time

# import requests
import boto3 as boto3

client = boto3.client('dynamodb')


def lambda_handler(event, context):
    slack_path = event["pathParameters"]["slack_path"]
    # TODO validate slack_path
    print(f"Got slack_path: {slack_path}")

    ttl_minutes = 5
    ttl = str(int(time.time() + ttl_minutes * 60))
    print(f"Calculated timestamp: {ttl}")

    response = client.update_item(
        TableName=os.environ["TABLE_NAME"],
        Key={"id": {
            "S": slack_path
        }},
        UpdateExpression="SET timetolive = :ttl",
        ExpressionAttributeValues={
            ":ttl": {
                "N": ttl
            }
        })

    print(f"Updated item in DynamoDB: {json.dumps(response)}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Updated entry",
        }),
    }
