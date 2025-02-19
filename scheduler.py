from apscheduler.schedulers.background import BackgroundScheduler
import alphavantage

news_data = None
top_20_gainers_losers = None

def scheduled_task():
    """ 매일 새벽 06:05에 실행할 함수 """
    news = alphavantage.get_news()
    top_20_gainers_losers = alphavantage.get_top_20_gainers_losers()

# 스케줄러 설정
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_task, "cron", hour=6, minute=5)  # 매일 06:05 실행

def start():
    scheduler.start()
