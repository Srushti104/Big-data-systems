import config
import torch
import flask
import time
from flask import Flask
from flask import request
from model import BERTBaseUncased
import functools
import torch.nn as nn


app = Flask(__name__)

MODEL = None
DEVICE = config.DEVICE
PREDICTION_DICT = dict()


def sentence_prediction(sentence):
    tokenizer = config.TOKENIZER
    max_len = config.MAX_LEN
    review = str(sentence)
    review = " ".join(review.split())

    inputs = tokenizer.encode_plus(
        review, None, add_special_tokens=True, max_length=max_len
    )

    ids = inputs["input_ids"]
    mask = inputs["attention_mask"]
    token_type_ids = inputs["token_type_ids"]

    padding_length = max_len - len(ids)
    ids = ids + ([0] * padding_length)
    mask = mask + ([0] * padding_length)
    token_type_ids = token_type_ids + ([0] * padding_length)

    ids = torch.tensor(ids, dtype=torch.long).unsqueeze(0)
    mask = torch.tensor(mask, dtype=torch.long).unsqueeze(0)
    token_type_ids = torch.tensor(token_type_ids, dtype=torch.long).unsqueeze(0)

    ids = ids.to(DEVICE, dtype=torch.long)
    token_type_ids = token_type_ids.to(DEVICE, dtype=torch.long)
    mask = mask.to(DEVICE, dtype=torch.long)

    outputs = MODEL(ids=ids, mask=mask, token_type_ids=token_type_ids)

    outputs = torch.sigmoid(outputs).cpu().detach().numpy()
    return outputs[0][0]


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
    #sentence = request.args.get("sentence")
        sentence = request.get_json()
        sentence= sentence["data"]
        print(sentence)
        response = {}
        response["input"] = {"data": sentence}
        response["pred"] = []
        for s in sentence:
            print(s)
            start_time = time.time()
            positive_prediction = sentence_prediction(s)
            negative_prediction = 1 - positive_prediction
            if positive_prediction>negative_prediction:
                prediction=positive_prediction
            else:
                prediction='-'+str(negative_prediction)
            response["pred"].append([str(prediction)])
        return flask.jsonify(response)

# @app.route("/predict")
# def predict():
#     sentence = request.args.get("sentence")
#     print(type(sentence))
#     start_time = time.time()
#     positive_prediction = sentence_prediction(sentence)
#         #sentence1 = sentence.get_json()
#     start_time = time.time()
#     positive_prediction = sentence_prediction(sentence)
#     negative_prediction = 1 - positive_prediction
#     response = {}
#     Input={}
#     # response["response"] = {
#     #     "positive": str(positive_prediction),
#     #     "negative": str(negative_prediction),
#     #     "sentence": str(sentence),
#     #     "time_taken": str(time.time() - start_time),
#     #
#     # }
#     # Input ={{
#     #     "data": [
#     #         str(sentence)
#     #     ]
#     #         }
#     response =   {
#             "input": {
#                 "data": [
#                     str(sentence)
#                 ]
#             },
#             "pred": [
#                 [
#                     str(positive_prediction)  # closer to 1 => positive
#                 ],
#                 [
#                     str(negative_prediction)  # closer to 0 => negative
#                 ]
#             ]
#         }
#     return flask.jsonify(response)


if __name__ == "__main__":
    MODEL = BERTBaseUncased()
    MODEL.load_state_dict(torch.load(config.MODEL_PATH))
    MODEL.to(DEVICE)
    MODEL.eval()
    app.run(host="0.0.0.0", port="5050", debug=True)


