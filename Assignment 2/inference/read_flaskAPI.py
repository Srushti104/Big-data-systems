
import pandas as pd
import requests
import json
from flask import jsonify

def read_scraped_csv(file):

    df = pd.read_csv(file)

    sentence = { "data": df['sentence'] }
    for key, value in sentence.items():

        return(value)

def read_inference_API(sentence):

    print("Hitting API to get inference of sentences")

    url = "http://127.0.0.1:5050/predict"

    payload = json.dumps({
      "data": [
        s for s in sentence
      ]
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    data = json.loads(response.text)

    return (data)


def json_to_csv(data):

    dataFrame_pred = pd.DataFrame(data['pred'])
    dataFrame_data = pd.DataFrame(data['input']['data'])

    dataFrame = pd.merge(dataFrame_data, dataFrame_pred, left_index=True, right_index=True)
    dataFrame.columns = ['Statement', 'Sentiment']
    print(dataFrame)

    # dataFrame['Sentiment'] = 'Positive' if int(dataFrame['Sentiment'].values) > 0 else 'Negative'
    #dataFrame['Sentiment'] = ['Positive' if dataFrame['Sentiment'][(dataFrame['Sentiment'].astype(float).any()) > 0] else 'Negative']
    #     dataFrame['Sentiment'] = 'Positive'
    # else:
    #     dataFrame['Sentiment'] = 'Negative'
    # dataFrame['Sentiment'][(dataFrame['Sentiment'].astype(float)) > 0] = 'Negative'


    dataFrame.to_csv('/Users/akshaybhoge/PycharmProjects/Edgar/inference/Inference-Labeled.csv', encoding='utf-8', index=False)

# if __name__ == '__main__':

    # sentence = read_scraped_csv('/Users/akshaybhoge/PycharmProjects/Edgar/inference/Inference-transcript.csv')
    # response = read_inference_API(sentence)
    # json_to_csv(response)
