import boto3

# Connect to Boto3
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2')

# Your Bucket goes here
bucket_name = ''

# Your S3 Path goes here
filename = ''


def download_from_s3(filename):
    s3.Bucket(bucket_name).download_file(Filename='my_downloaded_file', Key=filename)
    print('Download Complete')

# Call the function and get the file
download_from_s3(filename)
