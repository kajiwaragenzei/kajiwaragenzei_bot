import os
import requests
import tweepy
from datetime import datetime, timezone, timedelta
import feedparser
import random

def generate_tweet():
    
    api_key = os.getenv("GEMINI_API_KEY")
    # タイムゾーンを日本（JST）の日付文字列を生成
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)
    date_str = f"{now.month}月{now.day}日"
    greetings = [
        "税金高いっすね☆（気軽な挨拶）",
        "税金高いっすね🙋‍♂️（気さくな挨拶）",
        "税金高いっすね😎（ナウい挨拶）",
        "税金高いっすね😢（切ない挨拶）",
        "税金高いっすね🎊（めでたい挨拶）",
        "税金高いっすね🇯🇵（日本伝統の挨拶）",
        "税金高いっすね😍（メロメロな挨拶）",
    ]

    greeting = random.choice(descriptions)

    # ニュース取得
    # news = get_google_news_trends()
    # news_prompt_text = format_news_for_prompt(news)
    
    # Geminiへのプロンプト生成
    prompt = f"""
        あなたはXの投稿文を生成するAIです。
        以下の指示に従い、投稿文を140字以内で生成してください。

        1. **投稿の冒頭:** "{greeting}" を入れてください。
        2. **本文:** 本日の日付"{date_str}"が持つ何らかの意味（例: 誰かの誕生日、歴史上の出来事など）を短く紹介。
        3. **投稿の最後:** "今日も減税と社会保障費削減を進めましょう。ゲン税で日本をゲン気に！（AI自動化投稿）" を入れてください。
        4. **文字数:** 全体で140字以内であることを厳守してください。
        5. **出力:** 生成された投稿文のみを出力してください。
    """

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(url, headers=headers, params=params, json=data)
    if response.status_code != 200:
        raise RuntimeError(f"Gemini API error: {response.status_code} {response.text}")
    
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

import feedparser

def get_google_news_trends():
    rss_url = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(rss_url)

    news_items = []
    for entry in feed.entries[:5]:  # 最新5件を取得
        news_items.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'summary': entry.summary
        })
    
    return news_items

def format_news_for_prompt(news_items):
    prompt_lines = ["今日の注目ニュースはこちらです：\n"]
    for i, item in enumerate(news_items, 1):
        prompt_lines.append(f"{i}. {item['title']}")
    return "\n".join(prompt_lines)



def post_to_twitter(text):
    client = tweepy.Client(
        bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
        consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
        consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )
    response = client.create_tweet(text=text)
    print(f"ツイート成功: {response.data}")

if __name__ == "__main__":
    tweet = generate_tweet()
    print("生成されたツイート:", tweet)
    post_to_twitter(tweet)
