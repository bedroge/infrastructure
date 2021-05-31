import json
import logging
import os
import urllib3

# Read all the environment variables
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
OBJECT_TYPE = os.environ.get('OBJECT_TYPE', 'File')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def human_size(bytes, units=[' bytes','KB','MB','GB','TB', 'PB', 'EB']):
    """ Returns a human readable string representation of bytes """
    return str(bytes) + units[0] if bytes < 1024 else human_size(bytes>>10, units[1:])


def lambda_handler(event, context):
    logger.info("Event: " + str(event))

    # Find bucket name
    bucket = event['Records'][0]['s3']['bucket']['name']

    # Find details about object
    object_type = OBJECT_TYPE
    object_key = event['Records'][0]['s3']['object']['key']
    object_url = 'https://' + bucket + '.s3.amazonaws.com/' + object_key
    object_source = event['Records'][0]['requestParameters']['sourceIPAddress']
    event_time = event['Records'][0]['eventTime']

    action, reason = event['Records'][0]['eventName'].split(':')

    if action == 'ObjectCreated':
        # New file uploaded
        object_size = human_size(event['Records'][0]['s3']['object']['size'])
        attachment_title = f'New {object_type.lower()} uploaded! :tada:'
        message_title = f'{object_type} uploaded to bucket "{bucket}"'
        message_level = 'good'
        message = f'{object_key} has been uploaded to bucket on {event_time}\n file size: {object_size}\n URL: {object_url}\n source: {object_source}'

    elif action == 'ObjectRemoved':
        # Deleted an existing file
        if reason == 'Delete':
            attachment_title = f'Old {object_type.lower()} has been deleted!'
        elif reason == 'DeleteMarkerCreated':
            attachment_title = f'Delete marker created for {object_type}!'
        else:
            attachment_title = f'Reason: {reason}'

        message_title = f'{object_type} deleted from bucket "{bucket}"'
        message_level = 'warning'
        message = f'{object_key} has been deleted from bucket on {event_time}\n URL: {object_url}\n reason: {reason}'

    logger.info("Message: " + str(message))

    # Construct a Slack message
    slack_message = {
       "attachments":[
          {
             "fallback": attachment_title,
             "pretext": attachment_title,
             "color": message_level,
             "fields":[
                {
                   "title": message_title,
                   "value": message,
                   "short": False,
                }
             ]
          }
       ]
    }

    # Post message on Slack
    http = urllib3.PoolManager()
    encoded_data = json.dumps(slack_message).encode('utf-8')
    try:
        response = http.request("POST", SLACK_WEBHOOK_URL, body=encoded_data)
        logger.info("Message posted to Slack!")
    except urllib3.exceptions.HTTPError as err:
        logger.error("Failed to post message to Slack: %s", err)
