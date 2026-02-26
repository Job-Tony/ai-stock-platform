from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data.fetch_prices import get_stock_data
from sentiment.sentiment_analyzer import analyze_sentiment
from ml.random_forest import predict_trend
from trading.paper_trading import execute_trade
from chatbot.advisor_bot import chatbot_reply

app = FastAPI()

# =====================================
# CORS CONFIG (DEVELOPMENT SAFE)
# =====================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# ROOT
# =====================================
@app.get("/")
def root():
    return {
        "message": "AI Stock Platform API is running",
        "primary_endpoint": "/analyze/{symbol}",
        "example": "/analyze/AAPL"
    }

# =====================================
# ANALYSIS API
# =====================================
@app.get("/analyze/{symbol}")
def analyze(symbol: str):
    prices = get_stock_data(symbol)

    if prices is None or prices.empty:
        return {
            "symbol": symbol,
            "signal": "NO DATA",
            "prediction": 0.0,
            "sentiment": 0.0,
            "confidence": 0,
            "buy_score": 50
        }

    raw_pred = predict_trend(prices)
    sentiment = analyze_sentiment(symbol)

    # ---- SIGNAL LOGIC ----
    if raw_pred > 0.01:
        signal = "BUY"
    elif raw_pred < -0.01:
        signal = "SELL"
    else:
        signal = "HOLD"

    confidence = min(100, int(abs(raw_pred) * 2000))
    buy_score = normalize_buy_score(raw_pred, sentiment)

    return {
        "symbol": symbol,
        "signal": signal,
        "prediction": raw_pred,
        "sentiment": sentiment,
        "confidence": confidence,
        "buy_score": buy_score
    }

# =====================================
# PRICE DATA API (SAFE VERSION)
# =====================================
@app.get("/prices/{symbol}")
def get_prices(symbol: str):
    try:
        df = get_stock_data(symbol)

        if df is None or df.empty:
            return []

        # Ensure we have Close column
        if "Close" not in df.columns:
            return []

        # Reset index to make date a column
        df = df.reset_index()

        # Keep last 30 rows
        df = df.tail(30)

        # First column is usually Date after reset_index()
        date_column = df.columns[0]

        return [
            {
                "date": str(row[date_column]),
                "Close": float(row["Close"])
            }
            for _, row in df.iterrows()
        ]

    except Exception as e:
        print("Prices API error:", e)
        return []

# =====================================
# PAPER TRADING API
# =====================================
@app.post("/trade")
def trade(order: dict):
    return execute_trade(order)

# =====================================
# CHATBOT API
# =====================================
@app.post("/chat")
def chat(data: dict):
    return {"reply": chatbot_reply(data["message"])}

# =====================================
# BUY SCORE NORMALIZATION
# =====================================
def normalize_buy_score(prediction: float, sentiment: float) -> int:
    raw_score = prediction * sentiment
    raw_score = max(-0.05, min(0.05, raw_score))
    normalized = int(((raw_score + 0.05) / 0.10) * 100)
    return normalized