# Notifier for Staging S3 bucket

This Lambda function sends Slack notification whenever a file is being uploaded to or removed from the Staging S3 bucket.

## Setup

- Create a new Slack App, and set up an Incoming Webhook that allows the Lambda function to post messages to a certain channel.
- Create a new AWS Lambda function from scratch, and select Python 3.8 as runtime.
- Add the code from the file `lambda_function.py` to your new Lambda function, and hit `Deploy`.
- Go the Configuration page of your Lambda function, add an environment variable `SLACK_WEBHOOK_URL`, and set it to the URL obtained in the first step.
- Optionally, make an environment variable `OBJECT_TYPE` that has the name of the type of files that you are going to use, e.g. `Tarball`. This will be used in the messages. The default is `File`.
- You can test the Lambda function by making a new test template based on the existing templates `Amazon S3 Put/Delete`.
- Go to the S3 page, select your bucket, go to `Properties` and make a new event notification for all create and delete events; the destination should be set to your Lambda function.
