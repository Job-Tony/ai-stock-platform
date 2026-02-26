import requests
import time
from datetime import datetime, timedelta
from config import FINNHUB_API_KEY


def get_stock_data(symbol: str, limit: int = 30):

    if not FINNHUB_API_KEY:
        print("API key missing")
        return []

    # 🔥 Go back 120 days to ensure valid trading days
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=120)

    url = "https://finnhub.io/api/v1/stock/candle"

    params = {
        "symbol": symbol.upper(),
        "resolution": "D",
        "from": int(start_date.timestamp()),
        "to": int(end_date.timestamp()),
        "token": FINNHUB_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
    except Exception as e:
        print("Request failed:", e)
        return []

    # 🔎 Debug print
    if data.get("s") != "ok":
        print("Finnhub error:", data)
        return []

    prices = []

    for i in range(len(data["t"])):
        prices.append({
            "date": datetime.utcfromtimestamp(data["t"][i]).strftime('%Y-%m-%d'),
            "Open": float(data["o"][i]),
            "High": float(data["h"][i]),
            "Low": float(data["l"][i]),
            "Close": float(data["c"][i]),
            "Volume": float(data["v"][i])
        })

    return prices[-limit:]