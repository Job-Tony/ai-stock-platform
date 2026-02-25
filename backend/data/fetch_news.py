import requests
from config import FINNHUB_API_KEY


def fetch_news(symbol: str):
    """
    Fetch news headlines for a stock using Finnhub API.

    Returns:
    {
        "sentiment": float,   # placeholder (we use VADER later)
        "headlines": list[str]
    }
    """

    if not FINNHUB_API_KEY:
        return {"sentiment": 0.0, "headlines": []}

    url = "https://finnhub.io/api/v1/company-news"

    params = {
        "symbol": symbol,
        "from": "2024-01-01",   # you can dynamically compute this later
        "to": "2026-12-31",
        "token": FINNHUB_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
    except Exception:
        return {"sentiment": 0.0, "headlines": []}

    headlines = []

    for item in data[:10]:
        if "headline" in item:
            headlines.append(item["headline"])

    return {
        "sentiment": 0.0,  # We let VADER compute real sentiment
        "headlines": headlines
    }