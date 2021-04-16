import tensorflow as tf
import tensorflow_text as text
import boto3
import glob
import os
import pandas as pd
from io import StringIO
import json
import uvicorn

from fastapi import FastAPI

ACCESS_KEY = 'AKIAIN6VZUI6HDFIXJJA'
SECRET_KEY = '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'

app = FastAPI()

@app.get("/inference/")
def read_file(file:str):
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-2',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY)

    bucket_name = 'textfiles2'
    object_key = file+'.csv'

    client = boto3.client('s3',
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY
                          )

    csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')

    df = pd.read_csv(StringIO(csv_string))
    # print(df)
    res = []
    pred=[]
    json={}
    checkpoint = tf.saved_model.load('../albert_exported_model')
    for k,v in df.iterrows():
        print(v['Statement'])
        f = checkpoint.signatures["serving_default"]
        predict = f(tf.constant([v['Statement']]))
        print(float(predict['outputs']))
        res.append(v['Statement'])
        pred.append(float(predict['outputs']))

    return {

            'body': [{'sentence': s, 'prediction': p} for s, p in zip(res, pred)]

        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
