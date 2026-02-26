import requests
import time
from config import FINNHUB_API_KEY


def get_stock_data(symbol: str, limit: int = 30):
    """
    Fetch recent daily stock data from Finnhub.
    Returns list of dictionaries.
    """

    if not FINNHUB_API_KEY:
        print("FINNHUB_API_KEY not set")
        return []

    end_time = int(time.time())

    # 🔥 Go back 90 days to ensure enough market candles
    start_time = end_time - (90 * 86400)

    url = "https://finnhub.io/api/v1/stock/candle"

    params = {
        "symbol": symbol.upper(),
        "resolution": "D",
        "from": start_time,
        "to": end_time,
        "token": FINNHUB_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
    except Exception as e:
        print("Finnhub request failed:", e)
        return []

    # Debug if Finnhub rejects request
    if data.get("s") != "ok":
        print("Finnhub response:", data)
        return []

    prices = []

    timestamps = data.get("t", [])
    opens = data.get("o", [])
    highs = data.get("h", [])
    lows = data.get("l", [])
    closes = data.get("c", [])
    volumes = data.get("v", [])

    for i in range(len(timestamps)):
        try:
            prices.append({
                "date": time.strftime('%Y-%m-%d', time.gmtime(timestamps[i])),
                "Open": float(opens[i]),
                "High": float(highs[i]),
                "Low": float(lows[i]),
                "Close": float(closes[i]),
                "Volume": float(volumes[i])
            })
        except Exception:
            continue

    # Return only latest N candles
    return prices[-limit:]