import requests
from dotenv import load_dotenv

from data.data_store import news_data, top20_gainers_losers
from core.utils import get_time_range

def get_api_key():
  return os.getenv("API_KEY")


def get_news():
  # 환경변수 로드 및 API 키, 시간 범위 가져오기
  load_dotenv()
  api_key = get_api_key()
  time_from, time_to = get_time_range()

  BASE_URL = "https://www.alphavantage.co/query"
  combined_feed = []

  # 카테고리 코드 리스트 (총 15개)
  topics = [
    'blockchain', 'earnings',
    'ipo', 'mergers_and_acquisitions',
    'financial_markets', 'economy_fiscal',
    'economy_monetary', 'economy_macro',
    'energy_transportation', 'finance',
    'life_sciences', 'manufacturing',
    'real_estate', 'retail_wholesale',
    'technology'
  ]

  # 카테고리를 2개씩 묶어서 API 호출
  for i in range(0, len(topics), 2):
    # 만약 마지막 항목이 홀수라면 단일 요소로 사용
    pair = topics[i:i + 2]
    topics_param = ",".join(pair)
    print(f'API 호출 중: {topics_param}')

    params = {
      "function": "NEWS_SENTIMENT",
      "topics": topics_param,
      "limit": 100,
      "time_from": time_from,
      "time_to": time_to,
      "apikey": api_key
    }
    try:
      response = requests.get(BASE_URL, params=params)
      data = response.json()
    except Exception as e:
      print(f"API 호출 중 오류 발생 (topics: {topics_param}): {e}")
      continue

    if isinstance(data, dict) and "feed" in data:
      combined_feed.extend(data["feed"])
    else:
      print(f"유효한 feed 데이터가 없음 (topics: {topics_param})")

  # 최종 JSON 데이터 구조 생성
  final_data = {
    "items": str(len(combined_feed)),
    "feed": combined_feed
  }

  # 파일 저장: 현재 파일(__file__) 기준으로 core 폴더 내에 news_data.json 생성
  try:
    # 현재 __file__의 위치는 core 폴더 내부에 있으므로, 상위 폴더로 이동한 후 data 폴더를 지정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)
    file_path = os.path.join(parent_dir, "data", "news_data.json")

    with open(file_path, "w", encoding="utf-8") as file:
      json.dump(final_data, file, ensure_ascii=False, indent=4)
    print(f"뉴스 데이터 파일 생성 완료: {file_path}")
  except Exception as e:
    print(f"파일 저장 중 오류 발생: {e}")

  # 전역 변수 업데이트 (news_data는 feed 리스트만 저장)
  news_data.clear()
  news_data.extend(combined_feed)

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

