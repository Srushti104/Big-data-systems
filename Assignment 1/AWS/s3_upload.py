
import boto3

# Connect to Boto3
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-1')

bucket_name = 'glueblog-raws3bucket-qpsnkzcm2rj6'

s3.Bucket(bucket_name).upload_file(Filename="Data Files/CATALOG.csv", Key='data/' + "CATALOG.csv")
print ('Upload Complete')