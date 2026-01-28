import requests
from config import ALPHA_VANTAGE_KEY

def get_stock_data(symbol: str):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_KEY
    }

    r = requests.get(url, params=params)
    data = r.json()

    series = data.get("Time Series (Daily)", {})
    closes = [float(v["4. close"]) for v in list(series.values())[:30]]

    return closes[::-1]
