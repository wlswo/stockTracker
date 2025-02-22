import os

import requests
from dotenv import load_dotenv

from core.data_store import news_data, top20_gainers_losers
from core.utils import get_time_range

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
    "topics": "technology,finance",
    "limit": 10,
    "time_from": time_from,
    "time_to": time_to,
    "apikey": api_key
  }

  response = requests.get(BASE_URL, params=params)
  data = response.json()

  if isinstance(data, dict) and "feed" in data:
    news_data.clear()
    news_data.extend(data["feed"])
  else:
    news_data.clear()


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

  if isinstance(data, dict) and "top_gainers" in data and "top_losers" in data:
    top20_gainers_losers.clear()
    top20_gainers_losers.append(
        {"type": "gainers", "stocks": data["top_gainers"]})
    top20_gainers_losers.append(
        {"type": "losers", "stocks": data["top_losers"]})
  else:
    top20_gainers_losers.clear()

import json, os

def get_news_test():
  """
  news_data.json 파일에서 뉴스를 읽어와 반환합니다.
  """
  try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "news_data.json")
    with open(file_path, "r", encoding="utf-8") as file:
      data = json.load(file)
      if isinstance(data, dict) and "feed" in data:
        news_data.clear()
        news_data.extend(data["feed"])
      else:
        news_data.clear()
  except Exception as e:
    print(f"news_data.json 파일을 읽는 중 오류 발생: {e}")



def get_top_20_gainers_losers_test():
  """
  top20_gainers_losers.json 파일에서 상위 20 상승/하락 종목 데이터를 읽어와 반환합니다.
  """
  try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "top20_gainers_losers.json")
    with open(file_path, "r", encoding="utf-8") as file:
      data = json.load(file)
      if isinstance(data,
                    dict) and "top_gainers" in data and "top_losers" in data:
        top20_gainers_losers.clear()
        top20_gainers_losers.append(
            {"type": "gainers", "stocks": data["top_gainers"]})
        top20_gainers_losers.append(
            {"type": "losers", "stocks": data["top_losers"]})
      else:
        top20_gainers_losers.clear()
  except Exception as e:
    print(f"top20_gainers_losers.json 파일을 읽는 중 오류 발생: {e}")

