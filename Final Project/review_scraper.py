import json
import sys
import os
import requests
import datetime
import re
# import bs4 as BeautifulSoup
import csv
import time
from bs4 import BeautifulSoup as BeautifulSoup


def scrape_text(url):
    html_content = requests.get(url)
    html_content.raise_for_status()
    soup = BeautifulSoup(html_content.content, "lxml")
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
    print(new_d)

    review_cards = com_data.find_all('div', attrs={'class': 'review-content__body'})

    new_r = list()
    for i in range(len(review_cards)):
        new = review_cards[i].text.strip().lstrip().replace('\n', '')
        new_review = [new]
        new_r.append(new_review)
    print(new_r)

    x = zip(new_d, new_r)
    print(x)

    timestr = time.strftime("%Y%m%d")

    with open('bitcoin_review_' + timestr + '.csv', mode='w') as csv_file:
        fieldnames = ['date', 'body']
        writer = csv.writer(csv_file,  lineterminator='\n')
        writer.writerow(['date', 'body'])
        writer.writerows(x)


if __name__ == '__main__':
    scrape_text('https://www.trustpilot.com/review/bitcoin.com')