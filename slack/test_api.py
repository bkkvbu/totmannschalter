import unittest

from botocore.exceptions import ClientError

import slack.api
from slack.api import lambda_handler


def test_upsert_item(id: str, ttl: str, insert_if_not_exists: bool):
    return {}


def test_update_nonexisting_item(id: str, ttl: str, insert_if_not_exists: bool):
    if insert_if_not_exists:
        return {}
    else:
        raise ClientError({
            'Error': {
                'Code': 'ConditionalCheckFailedException',
                'Message': 'Details/context around the exception or error'
            },
            'ResponseMetadata': {
                'RequestId': '1234567890ABCDEF',
                'HostId': 'host ID data will appear here as a hash',
                'HTTPStatusCode': 400,
                'HTTPHeaders': {'header metadata key/values will appear here'},
                'RetryAttempts': 0
            }
        }, "UpdateItem")


class TestLambdaHandler(unittest.TestCase):

    def test_existing_entry(self):
        event = {
            'pathParameters': {
                'slack_path': 'foo/bar'
            }
        }
        slack.api.update_item = test_upsert_item

        self.assertIn('Updated entry', lambda_handler(event, None)['body'])

    def test_new_entry(self):
        event = {
            'pathParameters': {
                'slack_path': 'foo/bar'
            }
        }
        slack.api.update_item = test_update_nonexisting_item

        self.assertIn('Updated entry', lambda_handler(event, None)['body'])


if __name__ == '__main__':
    unittest.main()
