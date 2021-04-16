import json
import requests
import boto3
import pandas as pd
from io import StringIO
#

def token_generator():

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('grant_type', 'client_credentials'),
    )

    response = requests.post('https://lab-demo.auth.us-east-2.amazoncognito.com/oauth2/token',
                             headers=headers, params=params, auth=(
            '5se0740dmiqgp7iukb7pf7lrgu', '1drde3hvi0gnkgfu880tmr7rmvv5ai27bio8uqdi6sel1sglv0lu'))
    res =response.json()
    b= res['access_token']

    return b
# out_json={}
#
# ACCESS_KEY = 'AKIAIN6VZUI6HDFIXJJA'
# SECRET_KEY = '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'
#
# def read_file(file:str):
#     s3 = boto3.resource(
#         service_name='s3',
#         region_name='us-east-2',
#         aws_access_key_id=ACCESS_KEY,
#         aws_secret_access_key=SECRET_KEY)
#
#     bucket_name = 'textfiles2'
#     object_key = file+'.csv'
#
#     client = boto3.client('s3',
#                           aws_access_key_id=ACCESS_KEY,
#                           aws_secret_access_key=SECRET_KEY
#                           )
#
#     csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
#     body = csv_obj['Body']
#     csv_string = body.read().decode('utf-8')
#
#     df = pd.read_csv(StringIO(csv_string))
#     # print(df)
#     res = []
#     pred=[]
#
#
#     headers = {"content-type": "application/json"}
#
#     for k, v in df.iterrows():
#         text = v['Statement']
#
#         data = json.dumps({"signature_name": "serving_default", "instances": [text]})
#         # print(data)
#     # print('Data: {} ... {}'.format(data[:50], data[len(data)-52:]))
#
#         json_response = requests.post('http://localhost:8501/v1/models/saved_model:predict', data=data, headers=headers)
#         predictions = json.loads(json_response.text)
#         # print(json_response.text)
#         print(text)
#         print(predictions)
#
#
# read_file('AGEN')