import boto3
import glob
import os

def upload_to_s3():
    s3_bucket = 'textfiles2'
    s3_bucket_region = 'us-east-1'
    folder = 'call_transcripts'

    key_name = folder + '/'
    s3_connect = boto3.client('s3', s3_bucket_region)

    # upload File to S3
    for filename in os.listdir(folder):

        file_key_name = folder + '/' + filename
        local_path = os.getcwd()
        local_name = local_path + '/' + key_name + filename
        upload = s3_connect.upload_file(local_name, s3_bucket, file_key_name)

    print("Files uploaded in S3 bucket!")