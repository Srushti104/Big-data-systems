import streamlit as st
import boto3
import pandas as pd
import requests
import json
from io import StringIO
from boto3.dynamodb.conditions import Key
import os

verified = "True"

ACCESS_KEY = 'AKIAIN6VZUI6HDFIXJJA'
SECRET_KEY = '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'

Bearer = 'Bearer eyJraWQiOiJFWGJweG9JNnlaRHozT3M4M2Q4M0JlNnBYZUlLUTlaNVM2eXRpT0FqQjZNPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI1c2UwNzQwZG1pcWdwN2l1a2I3cGY3bHJndSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoibGFiLWFwaVwvbGFtYmRhLWludm9rZSIsImF1dGhfdGltZSI6MTYxODUzOTM2MCwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMi5hbWF6b25hd3MuY29tXC91cy1lYXN0LTJfczRnYWN0Zm1vIiwiZXhwIjoxNjE4NTQyOTYwLCJpYXQiOjE2MTg1MzkzNjAsInZlcnNpb24iOjIsImp0aSI6IjIyYzVkNWU1LWU0N2UtNGMxNS1hOWU0LTEwM2FjYzMyZWFkZSIsImNsaWVudF9pZCI6IjVzZTA3NDBkbWlxZ3A3aXVrYjdwZjdscmd1In0.DiTXsRA0Zuv6wrZBaf2WGGRsVltMuYz0n7s03oxEAw9rejcld7MwWWIf5FjvlcCtxAeOAofoigP7zNk0lkopgra1PyJIWMCUYI3E8DCJIAgzXLxwhyROtWRL_iHExUsulJpFdmP28shkAEojUf1Dg0ZQoVcjr7E-y50DT7foSIx1GGmTRQGds03Y650vH8xBuTbdKxb4WsawoiplhFVCIduEcmW1BCU7iALQMxdLMF6N9kE_9WNcp_Thg3ydGgtSes1i9CGz4mrJvPpp4lwa5AVwpf5nObrov-eTHLICMgLIKa6UVHhWtlSWyCYiotezYFccS6VnInNCrXNy5OAqwQ'


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
    res = response.json()
    b = res['access_token']

    return b

def read_username(username,password):
    resource = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id=ACCESS_KEY,
                              aws_secret_access_key=SECRET_KEY)
    table = resource.Table("Users")

    user = username+password
    response = table.query(
            KeyConditionExpression=Key('Login').eq(user)
        )
    return response['Items']

def read_file_json(s3_key):
    s3 = boto3.client(service_name='s3',
                      region_name='us-east-2',
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    print('Getting file %s..' % s3_key)
    obj = s3.get_object(Bucket="earnings-call-scraped", Key=s3_key)
    body = obj['Body'].read().decode(encoding="utf-8", errors="ignore")
    content_json = json.loads(body)
    return content_json


s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2'
    # aws_access_key_id=ACCESS_KEY,
    # aws_secret_access_key=SECRET_KEY
)


def read_file(s3_key):
    s3 = boto3.client(service_name='s3',
                      region_name='us-east-2')
                      # aws_access_key_id=ACCESS_KEY,
                      # aws_secret_access_key=SECRET_KEY)

    print('Getting file %s..' % s3_key)
    obj = s3.get_object(Bucket="earnings-call-scraped", Key=s3_key)
    body = obj['Body'].read().decode(encoding="utf-8", errors="ignore")
    return body

auth_user = token_generator()

def main():


    st.title("**_Anonymization using Amazon Comprehend_**")

    menu = ['User Authentication', "File Contents",  'Masking And Anonymization', 'Sentiment Analysis']
    choice = st.sidebar.selectbox("Menu", menu)

    st.markdown('<style>body{background-color: #FFF2C2;}</style>', unsafe_allow_html=True)

    key = []

    auth_user = token_generator()

    if choice == "File Contents":
        st.header("_File Contents_")
        st.markdown(
            """
            <span style="color:green"> </span>
            """,
            unsafe_allow_html=True)

        if st.button('Documentation'):
            st.write(
                f'<iframe src="http://127.0.0.1:8000/redoc", width=850, height=600  , scrolling=True></iframe>',
                unsafe_allow_html=True,
            )
        st.subheader("List of companies with Earnings Call")
        st.write('\n')
        s3 = boto3.resource('s3')
        my_bucket = s3.Bucket('textfiles2')


        for obj in my_bucket.objects.filter(Delimiter='/', Prefix='call_transcripts/'):
            key.append(obj.key[17:])
        # print(key[1:])

        filename = st.selectbox("Select Company to pick Earnings Call", key[1:])
        # token = st.text_input('token')
        bt_submit = st.button("Submit")

        if ((bt_submit) and (filename != "Select")):

            headers = {
                'Authorization': 'Bearer '+ auth_user}
            # API 1
            # base_url = 'http://127.0.0.1:8000/Edgar/'
            base_url = "https://9kf5kdc8w5.execute-api.us-east-2.amazonaws.com/test/Edgar/"
            # base_url = 'https://9kf5kdc8w5.execute-api.us-east-2.amazonaws.com/test/Edgar/'
            url = base_url + filename
            resp = requests.request("GET", url, headers=headers)
            # resp = requests.get(url, headers=headers)
            if (resp.status_code == 200):
                st.markdown(
                    """
                    <span style="color:green">STATUS CODE 200</span>
                    """,
                    unsafe_allow_html=True
                )
                # st.dataframe(resp.text.split('\\')[1:])
                print(resp.text)
                data_list = resp.json()

                st.subheader("File read Successfully!!")

                b = data_list['body']
                st.subheader(b)


        elif (filename == ""):
                st.markdown(
                    """
                    <span style="color:red">STATUS CODE 400</span>
                    """,
                    unsafe_allow_html=True)

    elif choice == 'Masking And Anonymization':

        s3 = boto3.resource('s3')
        my_bucket = s3.Bucket('textfiles2')

        st.header("_Masking And Anonymization_")
        # if st.button('Read Documentation'):
        #     st.write(
        #         f'<iframe src="http://localhost:8000/redoc", width=850, height=600  , scrolling=True></iframe>',
        #         unsafe_allow_html=True,
        #     )
        # st.write("Please select the entities to be recognized")
        for obj in my_bucket.objects.filter(Delimiter='/', Prefix='call_transcripts/'):
            key.append(obj.key[17:])
        filename = st.selectbox("Select Company to pick Earnings Call", key[1:])

        filepath = 's3%3A%2F%2Ftextfiles2%2Fcall_transcripts%2F'+filename

        mask = st.multiselect("Select entities to mask",
                                 ["NAME", "DATE", "ADDRESS", "SSN", "ID",
                                  "PHONE", "EMAIL", "PIN"])
        print(mask[i] for i in range(len(mask)))
        anonymize = st.multiselect("Select entities to anonymize",
                                   ["NAME", "DATE", "ADDRESS", "SSN", "ID",
                                     "PHONE", "EMAIL", "PIN"])
        print(anonymize[i] for i in range(len(anonymize)))

        # token = st.text_input('token')

        anonymize_string = ",".join(anonymize)
        mask_string = ",".join(mask)

        headers = {
            'Authorization': 'Bearer ' + auth_user}
        # API 1
        # base_url = 'http://127.0.0.1:8000/Edgar/'
        base_url = 'https://9kf5kdc8w5.execute-api.us-east-2.amazonaws.com/test/new?s3_path='+filepath +'&Mask_Entity='+mask_string+'&deidentify_Ent='+anonymize_string



        bt_submit = st.button("Submit")
        if (bt_submit):

            resp = requests.request("GET", base_url, headers=headers)

            content_json = resp.json()

            if (resp.status_code == 200):
                st.markdown(
                    """
                    <span style="color:green">STATUS CODE 200</span>
                    """,
                    unsafe_allow_html=True
                )
                b = content_json['body']
                st.subheader(b)

            else :
                st.markdown(
                    """
                    <span style="color:red">STATUS CODE 400</span>
                    """,
                    unsafe_allow_html=True

                )

    elif choice == 'User Authentication':

                # st.header('**_Deidentification System!_**')
                # image = Image.open('img-2.png')
                # st.image(image, caption='', use_column_width=True)
                st.write('\n')
                st.write('This application provides the user with a  data pipeline for masking \
                           and anonymizing private data contained in unstructured text. The four APIs provided\
                               maintain the workflow of the application. Click below to get started with the documentation.'
                         )
                if st.button('Documentation'):
                    st.write(
                        f'<iframe src="http://127.0.0.1:8000/redoc", width=850, height=600  , scrolling=True></iframe>',
                        unsafe_allow_html=True,
                    )

                st.header('_User Authentication_')

                st.subheader('_Please enter valid username and password_')

                username = st.text_input('Username')
                password = st.text_input('Password',type="password")
                submit = st.button("Submit")
                if username and password:
                    auth_user = read_username(username,password)

                    if submit and auth_user:
                    # auth_user_token = token_generator()
                     st.subheader("_User Authenticaticated!!_")
                    else:
                      st.subheader("_Invalid Username or password._")
                    # st.write(token)

    elif choice == 'Sentiment Analysis':
        st.header("_Sentiment Analysis on Anonymized and Masked data_")
        st.write('\n')
        s3 = boto3.resource('s3')
        my_bucket = s3.Bucket('textfiles2')

        for obj in my_bucket.objects.filter(Delimiter='/', Prefix='call_transcripts/'):
            key.append(obj.key[17:])
        # print(key[1:])

        filename = st.selectbox("Select Company to run sentiment analysis", key[1:])
        # bt_submit = st.button("Submit")

        if st.button("Submit") :
            bucket_name = 'textfiles2'
            object_key = filename + '.csv'

            client = boto3.client('s3',
                                  aws_access_key_id=ACCESS_KEY,
                                  aws_secret_access_key=SECRET_KEY
                                  )

            csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
            # if csv_obj['HTTPStatusCode'] == 200:
            body = csv_obj['Body']
            csv_string = body.read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_string))
            # print(df)
            headers = {"content-type": "application/json"}
            for k, v in df.iterrows():
                text = v['Statement']
                data = json.dumps({"signature_name": "serving_default", "instances": [text]})
                # print(data)
                # print('Data: {} ... {}'.format(data[:50], data[len(data)-52:]))
                json_response = requests.post('http://localhost:8501/v1/models/saved_model:predict', data=data,
                                              headers=headers)
                predictions = json.loads(json_response.text)
                # print(json_response.text)
                # print(text)
                # print(predictions)
                st.subheader(text)
                st.subheader(predictions)
            # else:
            #     st.markdown(
            #         """
            #         <span style="color:red">FILE NOT FOUND</span>
            #         """,
            #         unsafe_allow_html=True)


if __name__ == '__main__':
    main()