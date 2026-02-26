import requests
import time
from config import FINNHUB_API_KEY


def get_stock_data(symbol: str, limit: int = 30):
    """
    Fetch recent daily stock data from Finnhub.
    Returns list of dictionaries.
    """

    if not FINNHUB_API_KEY:
        return []

    end_time = int(time.time())
    start_time = end_time - (limit * 86400)

    url = "https://finnhub.io/api/v1/stock/candle"

    params = {
        "symbol": symbol,
        "resolution": "D",
        "from": start_time,
        "to": end_time,
        "token": FINNHUB_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
    except Exception:
        return []

    if data.get("s") != "ok":
        return []

    prices = []

    for i in range(len(data.get("t", []))):
        prices.append({
            "date": time.strftime('%Y-%m-%d', time.gmtime(data["t"][i])),
            "Open": float(data["o"][i]),
            "High": float(data["h"][i]),
            "Low": float(data["l"][i]),
            "Close": float(data["c"][i]),
            "Volume": float(data["v"][i])
        })

    return prices[-limit:]