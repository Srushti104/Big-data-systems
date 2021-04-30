import boto3
from fastapi import FastAPI
from mangum import Mangum
import datetime
import pandas as pd



s3 = boto3.client('s3',
                  region_name='us-east-2',
                  aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY)


app = FastAPI(debug=True)

@app.get("/")
def hello():
    return {"Hello": "World"}

@app.get("/bitcoin")
def bitcoin_range(File_Name: str, start_date:str, end_date:str):

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

@app.get("/todaySentiment")
def today_sentiment():

    newrev = []
    newdate = []

    bucket = 'bitcoin-prediction'
    filename = 'Bitcoin_sentiment.csv'

    obj = s3.get_object(Bucket=bucket, Key=filename)

    initial_df = pd.read_csv(obj['Body']) # 'Body' is a key word
    initial_df.drop('Unnamed: 0', axis = 1, inplace = True)

    date = initial_df['datetime'].tolist()

    for item in date:
        item = item.replace('[',"")
        item = item.replace(']', "")
        item = item.replace("'", "")
        newdate.append(item)

    review = initial_df['body'].tolist()

    for item in review:
        item = item.replace('[',"")
        item = item.replace(']', "")
        item = item.replace("'", "")
        newrev.append(item)

    sentiments = initial_df['Sentiment'].tolist()
    initial_df = pd.DataFrame((zip(newdate, newrev, sentiments)),
                 columns = ['date','review', 'sentiment'])

    initial_df = initial_df.to_json(orient="records")

    return {
        'Sentiments': initial_df
    }

@app.get("/allSentiments")
def all_reviews():

    newdate = []

    bucket = 'bitcoin-prediction'
    filename = 'review_sentiment.csv'
    obj = s3.get_object(Bucket = bucket, Key = filename)
    df = pd.read_csv(obj['Body'])
    date = df['date'].tolist()

    for item in date:
        item = item.replace('[',"")
        item = item.replace(']', "")
        item = item.replace("'", "")
        newdate.append(item)

    sentiments = df['sentiments'].tolist()
    df = pd.DataFrame((zip(newdate, sentiments)),
                 columns = ['date', 'sentiments'])

    finaldf = df.to_json(orient = "records")

    return {
        'Sentiments' : finaldf
    }

@app.get("/predictions")
def predictions():
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
