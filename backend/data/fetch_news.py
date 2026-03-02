import requests
from config import FINNHUB_API_KEY


def fetch_news(symbol: str):
    """
    Fetch news headlines for a symbol.
    Returns dict with:
    {
        "headlines": [...],
        "sentiment": 0.0   # Sentiment handled by VADER later
    }
    """

    if not FINNHUB_API_KEY:
        return {"sentiment": 0.0, "headlines": []}

    symbol = symbol.upper()

    # ==========================================
    # 🔥 SMART INDEX HANDLING
    # ==========================================

    # Indian indices → use NIFTY ETF proxy
    if symbol == "^NSEI":
        symbol = "NIFTYBEES.NS"

    elif symbol == "^BSESN":
        symbol = "SENSEXBEES.NS"

    # US index example
    elif symbol == "^GSPC":
        symbol = "SPY"

    # Commodities fallback (still generic)
    elif symbol in ["GC=F", "SI=F", "CL=F"]:
        return {
            "sentiment": 0.0,
            "headlines": [
                "Commodity markets reacting to macroeconomic data",
                "Global supply-demand dynamics influencing prices"
            ]
        }

    # ==========================================
    # FETCH NEWS
    # ==========================================

    url = "https://finnhub.io/api/v1/company-news"

    params = {
        "symbol": symbol,
        "from": "2025-01-01",
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
        if isinstance(item, dict) and item.get("headline"):
            headlines.append(item["headline"])

    return {
        "sentiment": 0.0,  # VADER computes real score
        "headlines": headlines
    }