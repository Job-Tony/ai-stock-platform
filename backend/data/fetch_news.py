import requests
from config import NEWS_API_KEY

def get_news(symbol: str):
    """
    Fetch recent news headlines for a stock symbol
    """
    if not NEWS_API_KEY:
        return []

    url = (
        "https://newsapi.org/v2/everything?"
        f"q={symbol}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception:
        return []

    articles = data.get("articles", [])
    headlines = [article["title"] for article in articles[:10] if "title" in article]

    return headlines
