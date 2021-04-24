import json
import sys
import os
import requests
import datetime
import re
# import bs4 as BeautifulSoup
from bs4 import BeautifulSoup as BeautifulSoup


def scrape_text(url):
    html_content = requests.get(url)
    html_content.raise_for_status()
    print(html_content.content)
    soup = BeautifulSoup(html_content.content, "lxml")
    com_data = soup.find('div', attrs={'class': 'review-list'})
    review_dates = com_data.find_all('div', attrs={'class': 'review-content-header__dates'})
    review_date = review_dates[0].find('script').string
    jsonObj = json.loads(review_date)
    new_dt = jsonObj['publishedDate'][:19]
    date = datetime.datetime.strptime(new_dt, "%Y-%m-%dT%H:%M:%S")

    review_cards = com_data.find_all('div', attrs={'class': 'review-content__body'})
    new = review_cards[0].text.strip().lstrip().replace('\n', '')

    response = {
        'date': str(date.strftime('%Y-%m-%d %H:%M:%S')),
        'body': new
    }


if __name__ == '__main__':
    response = scrape_text('https://www.trustpilot.com/review/bitcoin.com')