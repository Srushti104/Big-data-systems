
import datetime
import json
import os
import boto3
import pandas as pd
import io

bucket_name = os.environ['bucket_name']
dynamo_table = os.environ['dynamodb_table']

# Connect to S3
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-1')

# Connect to DynamoDB
resource = boto3.resource('dynamodb', region_name='us-east-1')

# Connect to the DynamoDB table
table = resource.Table(dynamo_table)


def getDynamoItems():

    try:

        resp = table.scan(AttributesToGet=['filename'])
        df2 = pd.DataFrame(resp['Items'])

        loaded_files = df2['filename'].unique()
    except:
        print ('Probably no loaded data on Dynamo')
    #     return empty list
        loaded_files = []
    return loaded_files

def load_dynamo(df):
    # Convert DF to a dictionary
    load_data = df.T.to_dict().values()

    # Load the table
    for i in load_data:
        table.put_item(Item=i)

    print ('Table Loaded')


def read_file(s3_key):
    s3 = boto3.client('s3')

    print ('Getting file %s..' % s3_key)
    obj = s3.get_object(Bucket=bucket_name, Key=s3_key)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))

    # Add the filename and current date & time to the dataframe
    df['filename'] = s3_key
    df['load_date'] = str(datetime.datetime.now())

    # Load the DynamoDB Table
    print('Loading file: %s' % s3_key)
    load_dynamo(df)


def service(event, context):
    # TODO implement
    my_bucket = s3.Bucket(bucket_name)


    loaded_files=getDynamoItems()
    # Filter the objects that we are interested in. In this case we'd just like files with load/data- prefix
    for object_summary in my_bucket.objects.filter(Prefix="load/data-"):
        print('Found file %s' % object_summary.key)

        if object_summary.key not in loaded_files:
            print ('%s does not exist on the table' % object_summary.key)
            read_file(object_summary.key)
        else:
            print ('%s already exists! File will be ignored' % object_summary.key)

    return {
        'statusCode': 200,
        'body': json.dumps('Process Complete')
    }
