import boto3
import pandas as pd
from io import StringIO

DYNAMODB = boto3.resource('dynamodb', region_name='us-east-2')
TABLE = DYNAMODB.Table("CommentTable")
QUEUE = "sentiment"
SQS = boto3.client("sqs", region_name='us-east-2')
comprehend = boto3.client(service_name='comprehend',region_name='us-east-2')


def scan_table(table):
    """Scans table and return results"""
    body=[]
    date=[]
    sentiments=[]
    response = table.scan()
    items = response['Items']

    for item in items:
        body.append(item['body'])
        date.append(item['Date'])

    for text in body:
        senti=(comprehend.detect_sentiment(Text=text, LanguageCode='en'))
        sentiments.append(senti['Sentiment'])

    df=pd.DataFrame(data=zip(date,body,sentiments),columns=['date','body','sentiments'])
    print(df)

    #df.to_csv('C:/Users/gnana/sentimentscores.csv',index=False)
    write_s3(df,'bitcoin-prediction','review')

def write_s3(df, bucket, name):
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)
        s3_resource = boto3.resource('s3')
        filename = f"{name}_sentiment.csv"
        res = s3_resource.Object(bucket, filename). \
            put(Body=csv_buffer.getvalue())


def lambda_handler(event, context):
    scan_table(table=TABLE)

