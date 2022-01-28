import os
# import requests
import time

import boto3

from notification import notify, expired_notification

client = boto3.client('dynamodb')


def lambda_handler(event, context):
    response = client.scan(
        TableName=os.environ["TABLE_NAME"],
        FilterExpression="#ttl < :now",
        ExpressionAttributeNames={
            "#ttl": "timetolive"
        },
        ExpressionAttributeValues={
            ":now": {
                "N": str(time.time())
            }
        }
    )

    items = response["Items"]

    print(f"Number of IDs to be processed: ${len(items)}")

    for item in items:
        id = item["id"]["S"]
        ttl = item["timetolive"]["N"]
        print(f"Processing id: {id}, expiry time: {ttl}")

        notify(id, expired_notification)

        client.delete_item(
            TableName=os.environ["TABLE_NAME"],
            Key={
                "id": {
                    "S": id
                }
            }
        )
