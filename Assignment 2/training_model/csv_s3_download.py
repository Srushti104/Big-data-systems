import boto3

# Connect to Boto3
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2')

# Your Bucket goes here
bucket_name = 'textfiles2'

# Your S3 Path goes here
filename = 'LabeledData/Labeled.csv'

def download_from_s3(filename):
    s3.Bucket(bucket_name).download_file(Filename='Labeled.csv', Key=filename)
    print('Download Complete')

# Call the function and get the file
# download_from_s3(filename)