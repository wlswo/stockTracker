import requests
import os
from dotenv import load_dotenv
from utils import get_time_range

def get_api_key():
    return os.getenv("API_KEY")

def get_news():
    load_dotenv()

    api_key = get_api_key()

    time_from, time_to = get_time_range()

    # get news
    BASE_URL = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "topics": "economy_macro",
        "limit": 10,
        "time_from": time_from,
        "time_to": time_to,
        "apikey": api_key
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    return data

#  get top 20 Gainers, Losers
def get_top_20_gainers_losers():
    load_dotenv()

    api_key = get_api_key()

    # get news
    BASE_URL = "https://www.alphavantage.co/query"
    params = {
        "function": "TOP_GAINERS_LOSERS",
        "apikey": api_key
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    return data