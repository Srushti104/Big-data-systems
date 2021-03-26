import boto3
import glob
import os

# Connect to Boto3
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2')

filename = 'model.bin'

def upload_model_to_s3(filename):
    s3_bucket = 'textfiles2'
    s3_bucket_region = 'us-east-1'

    s3.Bucket(s3_bucket).upload_file(Filename='/Users/akshaybhoge/PycharmProjects/Edgar/BERT_model/model.bin', Key='Model/' + filename)

    print("Model uploaded in S3 bucket!")

# upload_csv_to_s3(filename)