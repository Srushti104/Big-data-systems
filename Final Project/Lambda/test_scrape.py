import boto3
import json
import sys
import os
import requests
from bs4 import BeautifulSoup
from decimal import Decimal
import datetime

DYNAMODB = boto3.resource('dynamodb',region_name='us-east-2')
TABLE = DYNAMODB.Table("bitcoinlatest")
QUEUE = "testproducer"
SQS = boto3.client("sqs",region_name='us-east-2')

# SETUP LOGGING
import logging
from pythonjsonlogger import jsonlogger

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
LOG.addHandler(logHandler)


def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)


def scan_table(table):
    """Scans table and return results"""

    LOG.info(f"Scanning Table {table}")

    response = table.scan()
    items = response['Items']
    LOG.info(f"Found {len(items)} Items")
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    transform = yesterday.strftime("%b-%d-%Y")
    for daily in items:
        if daily['date'] == str(transform):
            return items[items.index(daily):(items.index(daily) + 1)]
    return items[-1:]


def send_sqs_msg(msg, queue_name, delay=0):
    """Send SQS Message
    Expects an SQS queue_name and msg in a dictionary format.
    Returns a response dictionary.
    """
    queue_url = SQS.get_queue_url(QueueName=queue_name)["QueueUrl"]
    queue_send_log_msg = "Send message to queue url: %s, with body: %s" % \
                         (queue_url, msg)
    LOG.info(queue_send_log_msg)

    json_msg = json.dumps(msg, default=default)
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
        pass


def scrape(url, dynamodb, table):
    html_content = requests.get(url)
    html_content.raise_for_status()

    soup = BeautifulSoup(html_content.text, "html.parser")

    btc_table = soup.find('table', attrs={'class': 'styled-table full-size-table'})
    btc_data = btc_table.tbody.find_all("tr")
    header = (btc_data[0].find_all("th"))

    headings = []
    for td in btc_data[0].find_all("th"):
        # remove any newlines and extra spaces
        headings.append(td.text.replace('\n', ' ').strip())

    data = {}
    # Get all the rows
    table_data = []
    for tr in btc_table.tbody.find_all("tr"):  # find all tr's from table's tbody
        t_row = {}
        # t_row = {'Date': '', 'Open': '', 'High': '', 'Close': '', 'Volume': '', 'Market Cap': ''}

        # find all td's(6) in tr and zip it with t_header
        for td, th in zip(tr.find_all("td"), headings):
            t_row[th] = td.text.replace('\n', '').strip().replace('$\u202f', '')
        table_data.append(t_row)
        pass
    table_data.pop(0)
    date_time_obj = datetime.datetime.strptime(table_data[0]['Date'], '%b %d, %Y')
    newformat = date_time_obj.strftime('%b-%d-%Y')

    response = table.put_item(
        Item={
            'date': str(newformat),
            'name': "Bitcoin",
            'Close': table_data[0]['Close'],
            'Open': table_data[0]['Open'],
            'High': table_data[0]['High'],
            'Low': table_data[0]['Low'],
            'Volume': table_data[0]['Volume'],
            'Marketcap': table_data[0]['Market Cap']
        }
    )


#scrape("https://coincodex.com/crypto/bitcoin/historical-data/", DYNAMODB, TABLE)
def lambda_handler(event, context):
    extra_logging = {"table": TABLE, "queue": QUEUE}
    LOG.info(f"event {event}, context {context}", extra=extra_logging)
    scrape("https://coincodex.com/crypto/bitcoin/historical-data/", DYNAMODB, TABLE)
    send_emissions(table=TABLE, queue_name=QUEUE)