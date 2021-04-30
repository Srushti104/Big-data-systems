import json
import boto3
import botocore
import pandas as pd
from io import StringIO

# S3 BUCKET
REGION = "us-east-2"


### SQS Utils###
# def sqs_queue_resource(queue_name):
#     sqs_resource = boto3.resource('sqs', region_name=REGION)
#     log_sqs_resource_msg = "Creating SQS resource conn with qname: [%s] in region: [%s]" % \
#                            (queue_name, REGION)
#
#     queue = sqs_resource.get_queue_by_name(QueueName=queue_name)
#     return queue
#
#
# def sqs_connection():
#     """Creates an SQS Connection which defaults to global var REGION"""
#
#     sqs_client = boto3.client("sqs", region_name=REGION)
#     log_sqs_client_msg = "Creating SQS connection in Region: [%s]" % REGION
#
#     return sqs_client
#
#
# def delete_sqs_msg(queue_name, receipt_handle):
#     sqs_client = sqs_connection()
#     try:
#         queue_url = sqs_client.get_queue_url(QueueName=queue_name)["QueueUrl"]
#         delete_log_msg = "Deleting msg with ReceiptHandle %s" % receipt_handle
#
#         response = sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
#     except botocore.exceptions.ClientError as error:
#         exception_msg = "FAILURE TO DELETE SQS MSG: Queue Name [%s] with error: [%s]" % \
#                         (queue_name, error)
#
#         return None
#
#     delete_log_msg_resp = "Response from delete from queue: %s" % response
#
#     return response


def comments_to_df(comments, dateList):
    finalList = []
    for i in range(len(comments)):
        element = [dateList[i], comments[i]]
        finalList.append(element)
        pass
    df = pd.DataFrame(finalList, columns=['datetime', 'body'])
    return df


def create_sentiment(row):
    """Uses AWS Comprehend to Create Sentiments on a DataFrame"""

    comprehend = boto3.client(service_name='comprehend')
    payload = comprehend.detect_sentiment(Text=row, LanguageCode='en')

    sentiment = payload['Sentiment']
    return sentiment


def apply_sentiment(df, column="body"):
    """Uses Pandas Apply to Create Sentiment Analysis"""

    df['Sentiment'] = df[column].apply(create_sentiment)
    return df


### S3 ###

def write_s3(df, bucket, name):
    """Write S3 Bucket"""

    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    filename = f"{name}_sentiment.csv"
    res = s3_resource.Object(bucket, filename). \
        put(Body=csv_buffer.getvalue())


def lambda_handler(event, context):
    """Entry Point for Lambda"""

    receipt_handle = event['Records'][0]['receiptHandle']  # sqs message
    # 'eventSourceARN': 'arn:aws:sqs:us-east-1:561744971673:producer'
    event_source_arn = event['Records'][0]['eventSourceARN']

    comments = []  # Captured from Queue
    dates = []

    # Process Queue
    for record in event['Records']:
        print(record)
        body = json.loads(record['body'])
        comment = body['body']
        datetime = body['Date']

        # Capture for processing
        comments.append(comment)
        dates.append(str(datetime))

        extra_logging = {"body": body, "comment": comment}

        qname = event_source_arn.split(":")[-1]
        extra_logging["queue"] = qname
    print(dates)
    print(comments)
        #res = delete_sqs_msg(queue_name=qname, receipt_handle=receipt_handle)

    df = comments_to_df(comments, dates)
    print(df)

    df = apply_sentiment(df)
    print(df)

    # Write result to S3
    write_s3(df=df, bucket="bitcoin-prediction", name='Bitcoin')