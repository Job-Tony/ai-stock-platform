import re
from data.fetch_prices import get_stock_data
from sentiment.sentiment_analyzer import analyze_sentiment
from ml.random_forest import predict_trend
from ml.risk_analyzer import calculate_risk

DEFAULT_STOCKS = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN", "GOOGL"]

# Only allow valid stock symbols
def extract_valid_symbol(message: str):
    words = re.findall(r"\b[A-Z]{1,5}\b", message.upper())
    for word in words:
        if word in DEFAULT_STOCKS:
            return word
    return None

def calculate_score(prediction, sentiment):
    return prediction * 0.7 + sentiment * 0.3

def generate_signal(prediction, sentiment):
    if prediction > 0.005 and sentiment > 0:
        return "BUY"
    elif prediction < -0.005 and sentiment < 0:
        return "SELL"
    else:
        return "HOLD"

def analyze_stock(symbol: str):
    prices = get_stock_data(symbol)
    if not prices or len(prices) < 20:
        return None

    prediction, _ = predict_trend(prices)
    sentiment = analyze_sentiment(symbol)
    risk = calculate_risk(prices)

    return {
        "symbol": symbol,
        "prediction": prediction,
        "sentiment": sentiment,
        "risk": risk,
        "score": calculate_score(prediction, sentiment),
        "signal": generate_signal(prediction, sentiment)
    }

def chatbot_reply(message: str):

    message = message.upper()

    # 1️⃣ Specific stock analysis
    symbol = extract_valid_symbol(message)
    if symbol:
        result = analyze_stock(symbol)

        if not result:
            return f"⚠️ Not enough data for {symbol}"

        return f"""
📊 {symbol} Analysis

Prediction: {round(result['prediction'],4)}
Sentiment: {round(result['sentiment'],3)}
Risk Level: {result['risk']}

👉 Recommendation: {result['signal']}
"""

    # 2️⃣ BEST BUY
    if "BUY" in message:
        results = []

        for sym in DEFAULT_STOCKS:
            try:
                res = analyze_stock(sym)
                if res:
                    results.append(res)
            except:
                pass

        if not results:
            return "Unable to analyze stocks at the moment."

        results.sort(key=lambda x: x["score"], reverse=True)
        best = results[0]

        return f"""
🔥 BEST STOCK TO BUY RIGHT NOW:

👉 {best['symbol']}

Prediction: {round(best['prediction'],4)}
Sentiment: {round(best['sentiment'],3)}
Risk: {best['risk']}
"""

    # 3️⃣ WORST (SELL)
    if "SELL" in message:

        results = []

        for sym in DEFAULT_STOCKS:
            try:
                res = analyze_stock(sym)
                if res:
                    results.append(res)
            except:
                pass

        if not results:
            return "Unable to analyze stocks at the moment."

        results.sort(key=lambda x: x["score"])
        worst = results[0]

        return f"""
⚠️ STOCK TO CONSIDER SELLING:

👉 {worst['symbol']}

Prediction: {round(worst['prediction'],4)}
Sentiment: {round(worst['sentiment'],3)}
Risk: {worst['risk']}
"""

    return """
Ask me:

• Which stock should I buy right now?
• Which stock should I sell?
• Analyze TSLA
• Is AAPL a good buy?
"""