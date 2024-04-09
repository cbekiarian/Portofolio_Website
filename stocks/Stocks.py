import requests
import datetime as dt
from datetime import timedelta
import os
import json

ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
URL_1 = "https://www.alphavantage.co/query"
URl_2 = "https://newsapi.org/v2/everything"


def get_news():
    now = dt.date.today()
    yesterday = str(now - timedelta(days=1))

    parameters2 = {
        "q": "tesla",
        "from": yesterday,
        "sortBy": "popularity",
        "apiKey": NEWS_API_KEY,
    }

    url2 = requests.get(url=URl_2, params=parameters2)
    url2.raise_for_status()
    article = url2.json()
    #
    # with open('data2.json', 'w') as f:
    #     json.dump(article, f)

    article = article["articles"][:10]
    return article
def check_stock(stock_name):

    stock = stock_name.capitalize()

    parameters1 = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock,
        "datatype": "json",
        "apikey": ALPHA_VANTAGE_API_KEY,
    }

    url = requests.get(url=URL_1, params=parameters1)
    print(url.raise_for_status())

    if url.raise_for_status():
        return 0
    url_json = url.json()
    #
    # with open('data.json', 'w') as f:
    #     json.dump(url_json, f)

    time_series = url_json["Time Series (Daily)"]
    today = dt.date.today()
    check_sunday = 0
    check_monday = 0
    check_tuesday = 0
    if today.weekday() == 6:
        check_sunday = 1
    if today.weekday() == 0:
        check_monday = 2
    if today.weekday() == 1:
        check_tuesday = 2

    yesterday = str(today - timedelta(days=1 + check_sunday + check_monday))
    b4_yesterday = str(today - timedelta(days=2 + check_sunday + check_monday + check_tuesday))

    value1 = time_series[yesterday]["4. close"]
    value2 = time_series[b4_yesterday]["4. close"]

    return [value1, value2]


class StocksInfo():

    def __init__(self, stock_name):
        self.stock = stock_name
        self.prices = check_stock(stock_name)
        self.news = get_news()

