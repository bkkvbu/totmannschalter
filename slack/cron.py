import os
import time

# import requests
import boto3
import requests

client = boto3.client('dynamodb')


def lambda_handler(event, context):
    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    current_time = time.time()
    response = client.scan(
        TableName=os.environ["TABLE_NAME"],
        FilterExpression="#ttl < :now",
        ExpressionAttributeNames={
            "#ttl": "timetolive"
        },
        ExpressionAttributeValues={
            ":now": {
                "N": str(current_time)
            }
        }
    )

    items = response["Items"]

    print(f"Number of IDs to be processed: ${len(items)}")

    for item in items:
        id = item["id"]["S"]
        ttl = item["timetolive"]["N"]
        print(f"Processing id: {id}, expiry time: {ttl}")
        try:
            requests.post(f'https://hooks.slack.com/services/{id}', json={
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": ":face_with_monocle: Something went wrong with your service! :worried: :fire: :boom:",
                            "emoji": True
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "accessory": {
                            "type": "image",
                            "image_url": f"https://random-d.uk/api/randomimg?t={current_time}",
                            "alt_text": "Cute duck"
                        },
                        "text": {
                            "type": "mrkdwn",
                            "text": "We did not hear from your service for the last 5min! :scream:\n\n*Please note:* This message will be sent just once. :nerd_face:"
                        }
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": ":skull_and_crossbones: Brought to you by http://www.totmannschalter.com"
                            }
                        ]
                    }
                ]
            })

        except ValueError:
            pass

        client.delete_item(
            TableName=os.environ["TABLE_NAME"],
            Key={
                "id": {
                    "S": id
                }
            }
        )
