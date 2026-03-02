from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict

from data.fetch_prices import get_stock_data
from data.fetch_news import fetch_news
from sentiment.sentiment_analyzer import analyze_sentiment
from ml.random_forest import predict_trend
from ml.risk_analyzer import calculate_risk
from trading.paper_trading import execute_trade, get_portfolio_summary
from chatbot.advisor_bot import chatbot_reply

app = FastAPI(title="AI Stock Investment Platform API")

# ======================================
# CORS
# ======================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================
# ROOT
# ======================================
@app.get("/")
def root():
    return {
        "status": "running",
        "api": "AI Stock Investment Platform",
        "available_endpoints": [
            "/analyze/{symbol}",
            "/prices/{symbol}",
            "/news/{symbol}",
            "/market-news",
            "/market-sentiment",
            "/trade",
            "/portfolio"
        ]
    }


# ======================================
# STOCK ANALYSIS
# ======================================
@app.get("/analyze/{symbol}")
def analyze(symbol: str):

    symbol = symbol.upper()

    try:
        prices = get_stock_data(symbol)

        if not prices:
            return JSONResponse(
                status_code=404,
                content={
                    "symbol": symbol,
                    "error": "No price data available"
                }
            )

        prediction, mae = predict_trend(prices)
        sentiment = analyze_sentiment(symbol)
        risk = calculate_risk(prices)

        # Signal Logic
        if prediction > 0.005 and sentiment > 0:
            signal = "BUY"
        elif prediction < -0.005 and sentiment < 0:
            signal = "SELL"
        else:
            signal = "HOLD"

        confidence = min(
            100,
            int((abs(prediction) + abs(sentiment)) * 5000)
        )

        buy_score = normalize_buy_score(prediction, sentiment)

        return {
            "symbol": symbol,
            "signal": signal,
            "prediction": round(prediction, 4),
            "sentiment": round(sentiment, 3),
            "confidence": confidence,
            "buy_score": buy_score,
            "risk_level": risk,
            "model_mae": mae
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# ======================================
# PRICE DATA
# ======================================
@app.get("/prices/{symbol}")
def prices(symbol: str):
    symbol = symbol.upper()
    try:
        return get_stock_data(symbol) or []
    except Exception:
        return []


# ======================================
# STOCK NEWS
# ======================================
@app.get("/news/{symbol}")
def news(symbol: str):
    symbol = symbol.upper()
    try:
        return fetch_news(symbol)
    except Exception:
        return {"headlines": [], "sentiment": 0.0}


# ======================================
# MARKET NEWS
# ======================================
@app.get("/market-news")
def market_news():
    try:
        return fetch_news("SPY")
    except Exception:
        return {"headlines": []}


# ======================================
# MARKET SENTIMENT
# ======================================
@app.get("/market-sentiment")
def market_sentiment():

    symbols = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]

    sentiments = []
    for s in symbols:
        try:
            sentiments.append(analyze_sentiment(s))
        except Exception:
            continue

    if not sentiments:
        return {"value": 0, "mood": "Unavailable"}

    avg = sum(sentiments) / len(sentiments)

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
def trade(order: Dict):
    return execute_trade(order)


@app.get("/portfolio")
def portfolio():
    return get_portfolio_summary()


# ======================================
# CHATBOT
# ======================================
@app.post("/chat")
def chat(data: Dict):
    message = data.get("message", "")
    if not message:
        return {"reply": "Please provide a message."}

    return {"reply": chatbot_reply(message)}


# ======================================
# BUY SCORE NORMALIZATION
# ======================================
def normalize_buy_score(prediction: float, sentiment: float) -> int:

    score = (prediction * 0.7) + (sentiment * 0.3)

    score = max(-0.05, min(0.05, score))

    normalized = int(((score + 0.05) / 0.10) * 100)

    return normalized