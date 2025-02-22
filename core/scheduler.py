from apscheduler.schedulers.background import BackgroundScheduler

from core.alphavantage import get_news, get_top_20_gainers_losers

# 스케줄러 설정
scheduler = BackgroundScheduler()
scheduler.add_job(get_news, "cron", hour=6, minute=5)  # 매일 06:05 실행
scheduler.add_job(get_top_20_gainers_losers, "cron", hour=6, minute=5)  # 매일 06:05 실행


def start():
  scheduler.start()


def shutdown():
  scheduler.shutdown()
