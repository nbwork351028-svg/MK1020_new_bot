import os
import requests
import feedparser

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

RSS_URL = "https://www.inform.kz/rss/rus.xml"

def translate_to_farsi(text):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "ru",
        "tl": "fa",
        "dt": "t",
        "q": text
    }
    r = requests.get(url, params=params, timeout=30)
    return r.json()[0][0][0]

rss = feedparser.parse(RSS_URL)

if rss.entries:
    news = rss.entries[0]

    title_ru = news.title
    link = news.link

    title_fa = translate_to_farsi(title_ru)

    message = f"📰 {title_fa}\n\n🔗 {link}"

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHANNEL_ID,
            "text": message
        },
        timeout=30
    )
