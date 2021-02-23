import requests
import os
import json

# Kafka Modules

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Enter your Bearer Token Here
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAEWjDQEAAAAA%2Bwd%2BmPyQn7TSYZpk5s5dcmjvwxE%3D2FwzRTJHibkSUA4vf4pq61tVZmTiQtA0aXoxgL3hHJtuk8846q'


def auth():
    return BEARER_TOKEN


def create_url():
    return "https://api.twitter.com/2/tweets/sample/stream"


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers, stream=True)
    print(response.status_code)
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json_response['data']['id'])

            id = str.encode(json_response['data']['id'])
            text = str.encode(json_response['data']['text'])

            # Publish the message to the broker
            producer.send('sample', key=id, value=text)
            print('Sent!')
            producer.flush()

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )


def main():
    bearer_token = auth()
    url = create_url()
    headers = create_headers(bearer_token)
    timeout = 0
    while True:
        connect_to_endpoint(url, headers)
        timeout += 1


if __name__ == "__main__":
    main()
