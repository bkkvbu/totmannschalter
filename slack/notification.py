import time

import requests

signature = {
    "type": "context",
    "elements": [
        {
            "type": "mrkdwn",
            "text": ":skull_and_crossbones: Brought to you by http://www.totmannschalter.com"
        }
    ]
}

random_duck = {
    "type": "image",
    "image_url": f"https://random-d.uk/api/randomimg?t={time.time()}",
    "alt_text": "Cute duck"
}

expired_notification = {
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
            "accessory": random_duck,
            "text": {
                "type": "mrkdwn",
                "text": "We did not hear from your service for the last 5min! :scream:\n\n*Please note:* This message will be sent just once. :nerd_face:"
            }
        },
        signature
    ]
}

newuser_notification = {
    "blocks": [

        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":hugging_face: Welcome! Successfully set up Totmannschalter! :hugging_face:",
                "emoji": True
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "accessory": random_duck,
            "text": {
                "type": "mrkdwn",
                "text": "We have received a first request from you! This means we're now on high alert and if you don't ping us at least every 5 minutes, we're going to use this same channel to tell you something is :fish:y"
            }
        },
        signature
    ]
}


def notify(path: str, body: object):
    try:
        requests.post(f'https://hooks.slack.com/services/{path}', json=body)

    except ValueError:
        pass
