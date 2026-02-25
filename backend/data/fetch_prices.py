import requests
import time
from config import FINNHUB_API_KEY


def get_stock_data(symbol: str, limit: int = 30):
    """
    Fetch recent daily stock data from Finnhub.

    Returns:
    [
      {
        date, Open, High, Low, Close, Volume
      }
    ]
    """

    end_time = int(time.time())
    start_time = end_time - (limit * 86400)  # last N days

    url = "https://finnhub.io/api/v1/stock/candle"

    params = {
        "symbol": symbol,
        "resolution": "D",  # Daily candles
        "from": start_time,
        "to": end_time,
        "token": FINNHUB_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
    except Exception:
        return []

    # Finnhub returns status in "s"
    if data.get("s") != "ok":
        return []

    prices = []

    for i in range(len(data["t"])):
        prices.append({
            "date": time.strftime('%Y-%m-%d', time.gmtime(data["t"][i])),
            "Open": float(data["o"][i]),
            "High": float(data["h"][i]),
            "Low": float(data["l"][i]),
            "Close": float(data["c"][i]),
            "Volume": float(data["v"][i])
        })

    # Ensure oldest → newest
    prices = prices[-limit:]

    return prices