import boto3
from datetime import datetime
import os


def upload_to_s3():
    # Connect to Boto3
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-2')

    # Replace this with your S3 Bucket
    bucket_name = ''

    model_files = [os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'retrained_graph_v2.pb')),
                   os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'retrained_labels.txt'))]
    for file in model_files:
        print(file)
        s3.Bucket(bucket_name).upload_file(Filename=file,
                                           Key='model/' + datetime.today().strftime(
                                               '%Y-%m-%d-%H:%M:%S') + '_' + os.path.basename(file))
        print('Upload Complete')
