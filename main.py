from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core import scheduler
from core.data_store import news_data, top20_gainers_losers

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
  """ FastAPI 애플리케이션의 라이프사이클 관리 """
  scheduler.start()
  yield
  scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")),
          name="static")

from core.alphavantage import get_news, get_top_20_gainers_losers, \
  get_news_test, get_top_20_gainers_losers_test


@app.get("/", response_class=HTMLResponse)
async def base(request: Request):
  """ HTML 페이지 렌더링 (전역 변수 데이터를 활용) """
  get_news_test()
  get_top_20_gainers_losers_test()

  return templates.TemplateResponse("index.html", {
    "request": request,
    "news": news_data,
    "top20_gainers_losers": top20_gainers_losers
  })


def main():
  """ FastAPI 실행 함수 """
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)


if __name__ == "__main__":
  main()
