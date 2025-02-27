from contextlib import asynccontextmanager
from pathlib import Path
from datetime import datetime
from typing import List

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from scheduler import scheduler
from data.data_store import news_data, top20_gainers_losers
from core.alphavantage import get_news_test, get_top_20_gainers_losers_test

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ FastAPI 애플리케이션의 라이프사이클 관리 (시작 시 스케줄러 실행, 종료 시 종료) """
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def sort_news(news_list: List[dict], sort_by: str):
    """ 정렬 기준에 따라 뉴스 데이터를 정렬합니다.
        - sort_by == "time": 최신순 (time_published: "YYYYMMDDTHHMMSS")
        - sort_by == "importance": 중요순 (importance_score 기준)
    """
    if sort_by == "time":
        def parse_time(item):
            try:
                return datetime.strptime(item.get("time_published", ""), "%Y%m%dT%H%M%S")
            except Exception:
                return datetime.min

        return sorted(news_list, key=parse_time, reverse=True)
    elif sort_by == "importance":
        return sorted(news_list, key=lambda x: x.get("importance_score", 0), reverse=True)
    else:
        return news_list


@app.get("/news", response_class=HTMLResponse)
async def base(
        request: Request,
        sort: str = Query("importance", description="정렬 기준: importance 또는 time"),
        page: int = Query(1, description="페이지 번호"),
        page_size: int = Query(10, description="한 페이지에 보여줄 뉴스 개수")
):
    """
    HTML 페이지 렌더링 (전역 변수 데이터를 활용하여 뉴스 데이터를 정렬 및 페이징)
    기본 정렬 기준은 'importance'입니다.
    """
    # 파일에 저장된 데이터를 읽어와 전역 변수 업데이트
    # get_news_test()
    # get_top_20_gainers_losers_test()

    # 정렬 및 페이징 처리
    sorted_news = sort_news(news_data, sort)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_news = sorted_news[start_idx:end_idx]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "news": paginated_news,
        "sort": sort,
        "page": page,
        "page_size": page_size,
        "top20_gainers_losers": top20_gainers_losers
    })


@app.get("/api/news", response_class=JSONResponse)
async def api_news(
        sort: str = Query("importance", description="정렬 기준: importance 또는 time"),
        page: int = Query(1, description="페이지 번호"),
        page_size: int = Query(10, description="한 페이지에 보여줄 뉴스 개수")
):
    """
    AJAX 호출용 API 엔드포인트:
    뉴스 데이터를 정렬 및 페이징 처리하여 JSON 형식으로 반환합니다.
    기본 정렬 기준은 'importance'입니다.
    """
    sorted_news = sort_news(news_data, sort)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_news = sorted_news[start_idx:end_idx]
    return {"news": paginated_news, "sort": sort, "page": page, "page_size": page_size}


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)


if __name__ == "__main__":
    main()
