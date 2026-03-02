import re
from data.fetch_prices import get_stock_data
from sentiment.sentiment_analyzer import analyze_sentiment
from ml.random_forest import predict_trend
from ml.risk_analyzer import calculate_risk

# Default stocks to scan
DEFAULT_STOCKS = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN", "GOOGL"]


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
    if not prices:
        return None

    prediction, _ = predict_trend(prices)
    sentiment = analyze_sentiment(symbol)
    risk = calculate_risk(prices)

    score = calculate_score(prediction, sentiment)
    signal = generate_signal(prediction, sentiment)

    return {
        "symbol": symbol,
        "prediction": prediction,
        "sentiment": sentiment,
        "risk": risk,
        "score": score,
        "signal": signal
    }


def chatbot_reply(message: str):

    message_upper = message.upper()

    # =====================================
    # 1️⃣ If user asked about specific symbol
    # =====================================
    match = re.findall(r"\b[A-Z]{1,5}\b", message_upper)
    if match:
        symbol = match[0]
        result = analyze_stock(symbol)

        if not result:
            return f"❌ No data available for {symbol}"

        return f"""
📊 {symbol} Analysis

Prediction: {round(result['prediction'],4)}
Sentiment: {round(result['sentiment'],3)}
Risk: {result['risk']}

👉 Recommendation: {result['signal']}
"""

    # =====================================
    # 2️⃣ If user asked WHICH STOCK TO BUY
    # =====================================
    if "BUY" in message_upper or "BEST STOCK" in message_upper:

        results = []
        for sym in DEFAULT_STOCKS:
            try:
                res = analyze_stock(sym)
                if res:
                    results.append(res)
            except:
                continue

        # sort highest score first
        results.sort(key=lambda x: x["score"], reverse=True)

        best = results[0]

        return f"""
🔥 BEST STOCK TO BUY RIGHT NOW:

👉 {best['symbol']}

Prediction: {round(best['prediction'],4)}
Sentiment: {round(best['sentiment'],3)}
Risk: {best['risk']}

Strongest combined AI score among tracked stocks.
"""

    # =====================================
    # 3️⃣ If user asked WHICH TO SELL
    # =====================================
    if "SELL" in message_upper:

        results = []
        for sym in DEFAULT_STOCKS:
            try:
                res = analyze_stock(sym)
                if res:
                    results.append(res)
            except:
                continue

        # sort lowest score first
        results.sort(key=lambda x: x["score"])

        worst = results[0]

        return f"""
⚠️ STOCK TO CONSIDER SELLING:

👉 {worst['symbol']}

Prediction: {round(worst['prediction'],4)}
Sentiment: {round(worst['sentiment'],3)}
Risk: {worst['risk']}

Weakest AI score among tracked stocks.
"""

    # =====================================
    # 4️⃣ Default fallback
    # =====================================
    return """
Ask me something like:

• Which stock should I buy right now?
• Which stock should I sell?
• Analyze TSLA
• Is AAPL a good buy?
"""