from fastapi import FastAPI
import alphavantage
import scheduler

app = FastAPI()

# FastAPI 서버 시작 시 스케줄러 실행
@app.on_event("startup")
def startup_event():
    scheduler.start()

@app.get("/")
async def base():
  return scheduler.news_data