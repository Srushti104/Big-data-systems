import boto3

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')


def get_sentiment(text):
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    response = dict(response)
    result = {}
    result["sentiment"] = response["Sentiment"]
    result["positive"] = response["SentimentScore"]["Positive"]
    result["negative"] = response["SentimentScore"]["Negative"]
    result["neutral"] = response["SentimentScore"]["Neutral"]
    result["mixed"] = response["SentimentScore"]["Mixed"]
    result["sentiment_score"] = (result["positive"] - result["negative"]) / 2
    return result






