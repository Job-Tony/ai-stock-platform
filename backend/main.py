from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data.fetch_prices import get_stock_data
from sentiment.sentiment_analyzer import analyze_sentiment
from ml.random_forest import predict_trend
from trading.paper_trading import execute_trade
from chatbot.advisor_bot import chatbot_reply

app = FastAPI()

# =========================
# CORS CONFIG (IMPORTANT)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow Netlify / browser access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "message": "AI Stock Platform API is running",
        "primary_endpoint": "/analyze/{symbol}",
        "example": "/analyze/AAPL"
    }

# =========================
# ANALYSIS API (PRIMARY)
# =========================
@app.get("/analyze/{symbol}")
def analyze(symbol: str):
    prices = get_stock_data(symbol)
    raw_pred = predict_trend(prices)
    sentiment = analyze_sentiment(symbol)

    confidence = max(0, min(100, int((raw_pred + 0.05) * 1000)))

    # Convert numeric prediction → signal
    if raw_pred > 0.01:
        signal = "BUY"
    elif raw_pred < -0.01:
        signal = "SELL"
    else:
        signal = "HOLD"

    buy_score = normalize_buy_score(raw_pred, sentiment)

    return {
        "symbol": symbol,
        "signal": signal,
        "prediction": raw_pred,
        "sentiment": sentiment,
        "confidence": confidence,
        "buy_score": buy_score
    }

# =========================
# PAPER TRADING API
# =========================
@app.post("/trade")
def trade(order: dict):
    return execute_trade(order)

# =========================
# CHATBOT API
# =========================
@app.post("/chat")
def chat(data: dict):
    return {"reply": chatbot_reply(data["message"])}

# =========================
# BUY SCORE NORMALIZATION
# =========================
def normalize_buy_score(prediction: float, sentiment: float) -> int:
    """
    prediction: typically small (-0.05 to +0.05)
    sentiment:  -1 to +1
    returns:    0 to 100
    """
    raw_score = prediction * sentiment

    # Clamp raw score to expected range
    raw_score = max(-0.05, min(0.05, raw_score))

    # Map -0.05 → 0 and +0.05 → 100
    normalized = int(((raw_score + 0.05) / 0.10) * 100)

    return normalized
