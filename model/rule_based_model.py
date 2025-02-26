import json
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data.data_store import keywords
import os

# 텍스트 정제 함수: 소문자화 및 특수문자 제거
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text


# 키워드 매칭 점수 계산 함수
def compute_keyword_score(text, keywords, weight=1):
    score = 0
    for kw in keywords:
        score += text.count(kw) * weight
    return score


# 뉴스 기사의 중요도 점수를 계산하는 함수
def compute_importance_score(news_item, keywords, tfidf_vectorizer, keyword_text, weights=(0.4, 0.3, 0.3)):
    # 제목과 요약 텍스트 정제
    title = clean_text(news_item['title'])
    summary = clean_text(news_item['summary'])

    # 제목과 요약에서 키워드 등장 빈도 계산 (제목은 가중치 2, 요약은 가중치 1 적용)
    title_keyword_score = compute_keyword_score(title, keywords, weight=2)
    summary_keyword_score = compute_keyword_score(summary, keywords, weight=1)
    keyword_score = title_keyword_score + summary_keyword_score

    # 키워드 점수를 sigmoid 함수를 통해 0~1 범위로 정규화
    normalized_keyword = 1 / (1 + np.exp(-keyword_score))

    # TF-IDF를 활용한 텍스트 유사도 계산
    news_text = title + " " + summary
    tfidf_matrix = tfidf_vectorizer.transform([news_text, keyword_text])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

    # 감성 점수 정규화 (-1~1 → 0~1)
    sentiment = news_item.get('overall_sentiment_score', 0)
    normalized_sentiment = (sentiment + 1) / 2

    # 각 요소에 가중치를 적용한 최종 중요도 점수 산출
    final_score = (normalized_keyword * weights[0]) + (similarity * weights[1]) + (normalized_sentiment * weights[2])
    return final_score


# JSON 파일에 저장된 뉴스 데이터를 업데이트하는 함수
def update_news_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)
    file_path = os.path.join(parent_dir, "data", "news_data.json")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"파일 읽기 실패: {e}")
        return

    feed = data.get("feed", [])

    # 키워드 텍스트: TF-IDF 계산용으로 키워드를 하나의 문자열로 결합
    keyword_text = " ".join(keywords)

    # TF-IDF 벡터라이저 학습: 모든 뉴스 텍스트(제목+요약)와 키워드 텍스트를 사용
    all_texts = [clean_text(item['title'] + " " + item['summary']) for item in feed]
    all_texts.append(keyword_text)
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectorizer.fit(all_texts)

    # 각 뉴스 기사에 대해 중요도 점수를 계산하여 데이터에 추가
    for item in feed:
        score = compute_importance_score(item, keywords, tfidf_vectorizer, keyword_text)
        item["importance_score"] = score

    # 업데이트된 데이터를 다시 JSON 파일에 저장
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"{len(feed)}개의 뉴스 항목에 중요도 점수를 업데이트했습니다. (파일: {file_path})")
    except Exception as e:
        print(f"파일 저장 실패: {e}")

