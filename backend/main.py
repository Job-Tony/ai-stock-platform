from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data.fetch_prices import get_stock_data
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
    return {"message": "AI Stock Platform API running"}

@app.get("/analyze/{symbol}")
def analyze(symbol: str):
    prices = get_stock_data(symbol)

    if not prices:
        return {
            "symbol": symbol,
            "signal": "NO DATA"
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

    confidence = min(
        100,
        int((abs(prediction) + abs(sentiment)) * 5000)
    )

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


@app.get("/prices/{symbol}")
def prices(symbol: str):
    return get_stock_data(symbol)


@app.post("/trade")
def trade(order: dict):
    return execute_trade(order)


@app.post("/chat")
def chat(data: dict):
    return {"reply": chatbot_reply(data["message"])}


def normalize_buy_score(prediction: float, sentiment: float) -> int:
    score = (prediction * 0.7) + (sentiment * 0.3)
    score = max(-0.05, min(0.05, score))
    return int(((score + 0.05) / 0.10) * 100)