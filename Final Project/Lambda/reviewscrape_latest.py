import boto3
import json
import sys
import os
import requests
import datetime
import re
from bs4 import BeautifulSoup
import pandas as pd

DYNAMODB = boto3.resource('dynamodb', region_name='us-east-2')
TABLE = DYNAMODB.Table("CommentTable")
QUEUE = "newsentiment"
SQS = boto3.client("sqs", region_name='us-east-2')
text = []
# SETUP LOGGING

import logging
from pythonjsonlogger import jsonlogger

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
LOG.addHandler(logHandler)


def scan_table(table):
    """Scans table and return results"""

    LOG.info(f"Scanning Table {table}")

    response = table.scan()
    items = response['Items']

    today = datetime.date.today()
    #yesterday = today - datetime.timedelta(days=1)
    transform = today.strftime('%Y-%m-%d')
    print(transform)
    # print(today)
    # print(yesterday)

    for item in items:
        new = (item['Date'])
        new = new.replace("'", '')
        new = new.replace("[", '')
        new = new.replace("]", '')
        new = new.split(" ", 1)
        new = new[0]
        # print(new)
        if new == str(transform):
            text.append(item)
        else:
            pass
    return text


def send_sqs_msg(msg, queue_name, delay=0):
    """Send SQS Message
    Expects an SQS queue_name and msg in a dictionary format.
    Returns a response dictionary.
    """
    queue_url = SQS.get_queue_url(QueueName=queue_name)["QueueUrl"]
    queue_send_log_msg = "Send message to queue url: %s, with body: %s" % \
                         (queue_url, msg)
    LOG.info(queue_send_log_msg)

    json_msg = json.dumps(msg)
    response = SQS.send_message(
        QueueUrl=queue_url,
        MessageBody=json_msg,
        DelaySeconds=delay)
    queue_send_log_msg_resp = "Message Response: %s for queue url: %s" % \
                              (response, queue_url)
    LOG.info(queue_send_log_msg_resp)
    return response


def send_emissions(table, queue_name):
    """Send Emissions"""

    items = scan_table(table=table)
    for item in items:
        LOG.info(f"Sending item {item} to queue: {queue_name}")
        response = send_sqs_msg(item, queue_name=queue_name)
        LOG.debug(response)


def scrape_text(url,dynamodb, table):
    html_content = requests.get(url)
    html_content.raise_for_status()
    soup = BeautifulSoup(html_content.text, "html.parser")
    com_data = soup.find('div', attrs={'class': 'review-list'})
    review_dates = com_data.find_all('div', attrs={'class': 'review-content-header__dates'})
    new_d = list()
    for i in range(len(review_dates)):
        review_date = review_dates[i].find('script').string
        jsonObj = json.loads(review_date)
        new_dt = jsonObj['publishedDate'][:19]
        date = datetime.datetime.strptime(new_dt, "%Y-%m-%dT%H:%M:%S")
        review_date = [str(date.strftime('%Y-%m-%d %H:%M:%S'))]
        new_d.append(review_date)
    review_cards = com_data.find_all('div', attrs={'class': 'review-content__body'})
    new_r = list()
    for i in range(len(review_cards)):
        new = review_cards[i].text.strip().lstrip().replace('\n', '')
        new_review = [new]
        new_r.append(new_review)
    x = zip(new_d, new_r)
    df = pd.DataFrame(list(zip(new_d, new_r)), columns=['date', 'body'])
    #return df:
    df['date'].to_string()
    listOfDict = []
    for index, row in df.iterrows():
        newDict = {'Date': '', 'text': ''}
        newDict['Date'] = row['date']
        newDict['text'] = row['body']
        listOfDict.append(newDict)
        pass

    for i in range(len(listOfDict)):
        response = table.put_item(
            Item={
                'Date': str(listOfDict[i]['Date']),
                'body': str(listOfDict[i]['text'])
            }
        )


def lambda_handler(event, context):
    extra_logging = {"table": TABLE, "queue": QUEUE}
    LOG.info(f"event {event}, context {context}", extra=extra_logging)
    scrape_text('https://www.trustpilot.com/review/bitcoin.com',DYNAMODB,TABLE)
    send_emissions(table=TABLE, queue_name=QUEUE)
