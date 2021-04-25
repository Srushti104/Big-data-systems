import json
import boto3
import pandas as pd
# from smart_open import smart_open

DYNAMODB = boto3.resource('dynamodb')


def convert(filename):
    final = pd.read_csv(filename, low_memory=False)

    listOfDict = []

    for index, row in final.iterrows():
        newDict = {'time': '', 'body': ''}
        newDict['Date'] = row['date']
        newDict['text'] = row['body']
        listOfDict.append(newDict)
        pass

    return listOfDict


def load(dictName, dynamodb):
    table = dynamodb.Table('CommentTable')

    for i in range(len(dictName)):
        response = table.put_item(
            Item={
                'Date': dictName[i]['Date'],
                'body': dictName[i]['text']
            }
        )


if __name__ == '__main__':
    load(convert("bitcoin_review_20210424.csv"), DYNAMODB)