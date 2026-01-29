import requests
from backend.config import ALPHA_VANTAGE_API_KEY


def fetch_news(symbol: str):
    """
    Fetch news + sentiment for a stock using Alpha Vantage NEWS_SENTIMENT.

    Returns:
    {
        "sentiment": float,   # average sentiment score (-1 to +1)
        "headlines": list[str]
    }
    """

    if not ALPHA_VANTAGE_API_KEY:
        return {"sentiment": 0.0, "headlines": []}

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception:
        return {"sentiment": 0.0, "headlines": []}

    feed = data.get("feed", [])

    sentiment_scores = []
    headlines = []

    for item in feed:
        # sentiment
        score = item.get("overall_sentiment_score")
        if score is not None:
            sentiment_scores.append(float(score))

        # headline text
        title = item.get("title")
        if title:
            headlines.append(title)

    avg_sentiment = (
        sum(sentiment_scores) / len(sentiment_scores)
        if sentiment_scores else 0.0
    )

    return {
        "sentiment": round(avg_sentiment, 3),
        "headlines": headlines[:10]
    }
