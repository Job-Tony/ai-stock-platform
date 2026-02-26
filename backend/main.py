from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data.fetch_prices import get_stock_data
from data.fetch_news import fetch_news
from sentiment.sentiment_analyzer import analyze_sentiment
from ml.random_forest import predict_trend
from ml.risk_analyzer import calculate_risk
from trading.paper_trading import execute_trade
from chatbot.advisor_bot import chatbot_reply

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "AI Stock Platform API running",
        "endpoints": [
            "/analyze/{symbol}",
            "/prices/{symbol}",
            "/news/{symbol}",
            "/market-news",
            "/market-sentiment"
        ]
    }


# ======================================
# STOCK ANALYSIS
# ======================================
@app.get("/analyze/{symbol}")
def analyze(symbol: str):

    prices = get_stock_data(symbol)

    if not prices:
        return {
            "symbol": symbol,
            "signal": "NO DATA",
            "prediction": 0.0,
            "sentiment": 0.0,
            "confidence": 0,
            "buy_score": 50,
            "risk_level": "Unknown",
            "model_mae": 0.0
        }

    prediction, mae = predict_trend(prices)
    sentiment = analyze_sentiment(symbol)
    risk = calculate_risk(prices)

    # Improved Signal Logic
    if prediction > 0.005 and sentiment > 0:
        signal = "BUY"
    elif prediction < -0.005 and sentiment < 0:
        signal = "SELL"
    else:
        signal = "HOLD"

    confidence = min(100, int((abs(prediction) + abs(sentiment)) * 5000))

    buy_score = normalize_buy_score(prediction, sentiment)

    return {
        "symbol": symbol,
        "signal": signal,
        "prediction": prediction,
        "sentiment": sentiment,
        "confidence": confidence,
        "buy_score": buy_score,
        "risk_level": risk,
        "model_mae": mae
    }


# ======================================
# PRICE DATA
# ======================================
@app.get("/prices/{symbol}")
def prices(symbol: str):
    return get_stock_data(symbol)


# ======================================
# STOCK NEWS
# ======================================
@app.get("/news/{symbol}")
def news(symbol: str):
    return fetch_news(symbol)


# ======================================
# MARKET NEWS (Using SPY)
# ======================================
@app.get("/market-news")
def market_news():
    return fetch_news("SPY")


# ======================================
# MARKET SENTIMENT
# ======================================
@app.get("/market-sentiment")
def market_sentiment():

    symbols = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]

    total = 0
    count = 0

    for s in symbols:
        sentiment = analyze_sentiment(s)
        total += sentiment
        count += 1

    avg = total / count if count else 0

    if avg > 0.05:
        mood = "Bullish 📈"
    elif avg < -0.05:
        mood = "Bearish 📉"
    else:
        mood = "Neutral ⚖️"

    return {
        "value": round(avg, 3),
        "mood": mood
    }


# ======================================
# PAPER TRADING
# ======================================
@app.post("/trade")
def trade(order: dict):
    return execute_trade(order)


# ======================================
# CHATBOT
# ======================================
@app.post("/chat")
def chat(data: dict):
    return {"reply": chatbot_reply(data["message"])}


# ======================================
# BUY SCORE
# ======================================
def normalize_buy_score(prediction: float, sentiment: float) -> int:
    score = (prediction * 0.7) + (sentiment * 0.3)

    score = max(-0.05, min(0.05, score))

    normalized = int(((score + 0.05) / 0.10) * 100)

    return normalized