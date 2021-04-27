import boto3
from fastapi import FastAPI
from mangum import Mangum
import datetime
import pandas as pd


ACCESS_KEY = 'AKIAWKCAZTNP6OC5P2VD'
SECRET_KEY = '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'

s3 = boto3.client('s3',
                  region_name='us-east-2',
                  aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY)


app = FastAPI(debug=True)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/bitcoin")
def read_file(File_Name: str, start_date:str, end_date:str):

    DYNAMODB = boto3.resource('dynamodb',
                              region_name='us-east-2',
                              aws_access_key_id=ACCESS_KEY,
                              aws_secret_access_key=SECRET_KEY)

    TABLE = DYNAMODB.Table("bitcoinlatest")
    response = TABLE.scan()
    items = response['Items']
    bitcoin=[]

    start_date = datetime.datetime.strptime(start_date, '%b-%d-%Y')
    end_date = datetime.datetime.strptime(end_date, '%b-%d-%Y')


    for item in items:
        date = ((item['date']))
        datetime_object = datetime.datetime.strptime(date, '%b-%d-%Y')
        if (datetime_object > start_date and datetime_object <= end_date):
            bitcoin.append(item)
        else:
            pass

    return {
        'body': (bitcoin)
    }

@app.get("/today")
def today():

    bucket = 'bitcoin-prediction'
    filename = 'Bitcoin_sentiment.csv'

    obj = s3.get_object(Bucket=bucket, Key=filename)

    initial_df = pd.read_csv(obj['Body']) # 'Body' is a key word

    initial_df = initial_df.to_json(orient="records")

    return {
        'Sentiments': (initial_df)
    }

@app.get("/allsentiments")
def reviews():

    newdate = []

    bucket = 'bitcoin-prediction'
    filename = 'review_sentiment.csv'
    obj = s3.get_object(Bucket=bucket, Key=filename)

    df = pd.read_csv(obj['Body']) # 'Body' is a key word

    date = df['date'].tolist()

    for item in date:
        item = item.replace('[',"")
        item = item.replace(']', "")
        item = item.replace("'", "")
        print(item)
        newdate.append(item)

    sentiments = df['sentiments'].tolist()
    df = pd.DataFrame((zip(newdate, sentiments)),
                 columns = ['date', 'sentiments'])

    finaldf = df.to_json(orient = "records")
    print(finaldf)

    return {
        'Sentiments' : finaldf
    }

@app.get("/Predictions")
def predict():
    newPred = []

    bucket = 'bitcoin-prediction'
    filename = 'predictions/30_pred.csv'
    obj = s3.get_object(Bucket=bucket, Key=filename)
    df = pd.read_csv(obj['Body'])  # 'Body' is a key word
    Pred = df['Pred'].tolist()

    for item in Pred:
        item = item.replace('[',"")
        item = item.replace(']', "")
        item = item.replace("'", "")
        newPred.append(item)

    date = df['Date'].tolist()

    df = pd.DataFrame((zip(date, newPred)),
                 columns=['date', 'Predictions'])

    predictions = df.to_json(orient="records")

    return {
        'Predictions' : predictions
    }

handler = Mangum(app)