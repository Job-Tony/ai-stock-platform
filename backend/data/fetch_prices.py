import requests
from backend.config import ALPHA_VANTAGE_API_KEY


def get_stock_data(symbol: str, limit: int = 30):
    """
    Fetch recent daily stock data from Alpha Vantage.

    Returns a list of dicts:
    [
      {
        date, Open, High, Low, Close, Volume
      }
    ]
    """

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception:
        return []

    series = data.get("Time Series (Daily)")
    if not series:
        return []

    prices = []

    for date, values in list(series.items())[:limit]:
        prices.append({
            "date": date,
            "Open": float(values["1. open"]),
            "High": float(values["2. high"]),
            "Low": float(values["3. low"]),
            "Close": float(values["4. close"]),
            "Volume": float(values["6. volume"])
        })

    # Oldest → newest (important for ML & meter animation)
    prices.reverse()
    return prices
