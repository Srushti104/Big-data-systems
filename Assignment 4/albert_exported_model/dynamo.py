import boto3
from boto3.dynamodb.conditions import Key
import json

ACCESS_KEY = 'AKIAIN6VZUI6HDFIXJJA'
SECRET_KEY = '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'

def read_username(username,password):
    resource = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id=ACCESS_KEY,
                              aws_secret_access_key=SECRET_KEY)
    table = resource.Table("Users")

    user = username+password
    response = table.query(
            KeyConditionExpression=Key('Login').eq(user)
        )
    return response['Items']

if __name__ == '__main__':
        movies = read_username('admin','qwerty')
        if movies:
            print(movies)