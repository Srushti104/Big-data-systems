import boto3
import glob
import os

# Connect to Boto3
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2')

filename = 'Labeled.csv'

def upload_csv_to_s3(filename):
    s3_bucket = 'textfiles2'
    s3_bucket_region = 'us-east-1'
    folder = 'call_transcripts'

    s3.Bucket(s3_bucket).upload_file(Filename=filename, Key='LabeledData/' + filename)

    print("CSV file uploaded in S3 bucket!")

upload_csv_to_s3(filename)