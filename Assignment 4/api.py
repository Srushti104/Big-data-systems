import boto3
from fastapi import FastAPI
import json
from mangum import Mangum
import hashlib
import uuid
import os
import logging
from fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser, CognitoClaims

ACCESS_KEY = 'AKIAIN6VZUI6HDFIXJJA'
SECRET_KEY = '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'
ddb = boto3.client('dynamodb', region_name='us-east-2', aws_access_key_id=ACCESS_KEY,
                   aws_secret_access_key=SECRET_KEY)
comprehend = boto3.client(service_name='comprehend', region_name='us-east-2', aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY)
client = boto3.client(service_name='comprehendmedical', region_name='us-east-2', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
os.environ["EntityMap"] = 'EntityMap'


def extract_entities_from_message(message):
    return client.detect_phi(Text=message)

def mask(i, entity_list, Mask_Entity):
    masked_message = mask_entities_in_message(i, entity_list, Mask_Entity)
    return masked_message

def mask_entities_in_message(message, entity_list, Mask_Entity):
    for entity in entity_list:
        check = any(item in entity['Type'] for item in Mask_Entity)
        if check is True:
            # if (entity['Type'] == Mask_Entity):
            message = message.replace(entity['Text'], '#' * len(entity['Text']))
    return message

def anonamizing(message, entity_list, deidentify_Ent):
    # Mask entities
    try:
        deidentified_message, entity_map = deidentify_entities_in_message(message, entity_list, deidentify_Ent)
        hashed_message = store_deidentified_message(deidentified_message, entity_map, os.environ['EntityMap'])
        # print(deidentified_message)
        #deidentifiedmessage.append(deidentified_message)
        # print(entity_map)
        return {
            "deid_message": deidentified_message,
            "hashed_message": hashed_message
        }
    except Exception as e:
        logging.error('Exception: %s. Unable to extract entities from message' % e)
        raise e

def deidentify_entities_in_message(message, entity_list, deidentify_Ent):
    entity_map = dict()
    for entity in entity_list:
        check = any(item in entity['Type'] for item in deidentify_Ent)
        if check is True:
            # if (entity['Type'] == deidentify_Ent):
            salted_entity = entity['Text'] + str(uuid.uuid4())
            hashkey = hashlib.sha3_256(salted_entity.encode()).hexdigest()
            entity_map[hashkey] = entity['Text']
            message = message.replace(entity['Text'], hashkey)
    return message, entity_map

def store_deidentified_message(message, entity_map, ddb_table):
    hashed_message = hashlib.sha3_256(message.encode()).hexdigest()
    for entity_hash in entity_map:
        ddb.put_item(
            TableName=ddb_table,
            Item={
                'MessageHash': {
                    'S': hashed_message
                },
                'EntityHash': {
                    'S': entity_hash
                },
                'Entity': {
                    'S': entity_map[entity_hash]
                }
            }
        )
    return hashed_message

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/Edgar/{File_Name}")
def read_file(File_Name: str):
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    bucket = 'textfiles2'
    filename = 'call_transcripts/' + File_Name + ''
    obj = s3.Object(bucket, filename)
    body = obj.get()['Body'].read()
    file = []
    res = []
    for line in body.splitlines():
        file.append((line.decode('utf8')))
    for text in file:
        if text.strip():
            res.append(text)
    return {
        'body': json.dumps(res)
    }

@app.get("/Edgar")
def PII_entities(s3_path: str):
    print(s3_path)
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-2', aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY)
    if s3_path.startswith('s3'):
        s3_path = s3_path[5:]
    s3_path = s3_path.split('/')
    bucket = s3_path[0]
    s3_key = ""
    if len(s3_path) > 1:
        s3_key = '/'.join(s3_path[1:])
    print(bucket)
    print(s3_key)
    res = []
    obj = s3.Object(bucket, s3_key)
    body = obj.get()['Body'].read()
    file = []
    for line in body.splitlines():
        file.append((line.decode('utf8')))
    for text in file:
        if text.strip():
            res.append(text)
    print(res)
    entity_list = []
    for text in res:
        text_PII = text
        entities_response = comprehend.detect_pii_entities(Text=text_PII, LanguageCode='en')
        e = entities_response['Entities']
        entity_list.append(e)
    print(entity_list)
    return {
        'body': json.dumps(entity_list)
    }

@app.get("/new")
def ananomize(s3_path: str, Mask_Entity: str, deidentify_Ent: str):
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-2', aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY)
    if s3_path.startswith('s3'):
        s3_path = s3_path[5:]
    s3_path = s3_path.split('/')
    bucket = s3_path[0]
    filename = s3_path[2]
    s3_key = ""
    if len(s3_path) > 1:
        s3_key = '/'.join(s3_path[1:])
    # print(bucket)
    # print(s3_key)
    obj = s3.Object(bucket, s3_key)
    body = obj.get()['Body'].read().decode('utf8')
    masked = []
    deidentified_list = []
    # deidentifiedmessage= str
    Mask_Entity = Mask_Entity.split(',')
    deidentify_Ent = deidentify_Ent.split(',')
    # print(deidentify_Ent)
    # print(Mask_Entity)
    # print(type(body))
    entities_response = extract_entities_from_message(body)
    entity_list = entities_response['Entities']
    masked.append(mask(body, entity_list, Mask_Entity))
    #print(type(masked))
    for message in masked:
        masked_entities_response = extract_entities_from_message(message)
        masked_entity_list = masked_entities_response['Entities']
        x = anonamizing(message, masked_entity_list, deidentify_Ent)
        deidentifiedmessage = (x['deid_message'])
    BUCKET_NAME = "textfiles2"
    OUTPUT_BODY = deidentifiedmessage
    s3.Bucket(BUCKET_NAME).put_object(Key=f'maskoutput/anaonamized.txt', Body=OUTPUT_BODY)
    #BUCKET_NAME = "textfiles2"
    #OUTPUT_NAME = f"maskoutput/" + filename + ".json"
    #OUTPUT_BODY = json.dumps(deidentifiedmessage)
    #s3.Bucket(BUCKET_NAME).put_object(Key=OUTPUT_NAME, Body=OUTPUT_BODY)

    # print((deidentifiedmessage))
    # for line in deidentifiedmessage.splitlines():
    #     if len(line) > 0:
    #         deidentified_list.append(line)
    #     else:
    #         pass
    # df = pd.DataFrame()
    # df['Statement'] = deidentified_list
    # print(df)
    # # Converting the dataframe to csv and storing it in S3 bucket
    # df_final = StringIO()
    # df.to_csv(df_final, header=True, index=False)
    # df_final.seek(0)
    # client = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
    #                       aws_secret_access_key=SECRET_KEY)
    # client.put_object(Bucket='textfiles2', Body=df_final.getvalue(), Key='anonymised.csv')
    return {
        'body': json.dumps(deidentifiedmessage)
    }

handler = Mangum(app)
