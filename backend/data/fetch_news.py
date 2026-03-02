import requests
from config import FINNHUB_API_KEY

def fetch_news(symbol: str):

    # Handle indices & commodities separately
    if symbol.startswith("^") or symbol in ["GC=F", "SI=F"]:
        return {
            "sentiment": 0.0,
            "headlines": [
                "Global market conditions impacting index movement",
                "Macroeconomic data influencing overall trend"
            ]
        }

    if not FINNHUB_API_KEY:
        return {"sentiment": 0.0, "headlines": []}

    url = "https://finnhub.io/api/v1/company-news"

    params = {
        "symbol": symbol,
        "from": "2024-01-01",
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
        "sentiment": 0.0,
        "headlines": headlines
    }