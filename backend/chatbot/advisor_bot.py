import re
from data.fetch_prices import get_stock_data
from sentiment.sentiment_analyzer import analyze_sentiment
from ml.random_forest import predict_trend
from ml.risk_analyzer import calculate_risk

DEFAULT_STOCKS = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN", "GOOGL"]


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


def explain_reason(prediction, sentiment, risk, signal):

    reasons = []

    if prediction > 0:
        reasons.append("Upward predicted price trend")
    else:
        reasons.append("Downward predicted price momentum")

    if sentiment > 0:
        reasons.append("Positive market/news sentiment")
    else:
        reasons.append("Negative market sentiment")

    if risk == "Low":
        reasons.append("Low volatility risk")
    elif risk == "High":
        reasons.append("High volatility risk")

    explanation = " • ".join(reasons)

    return f"""
Reasoning:
{explanation}

AI Conclusion: {signal}
"""


def analyze_stock(symbol: str):

    prices = get_stock_data(symbol)
    if not prices or len(prices) < 20:
        return None

    prediction, _ = predict_trend(prices)
    sentiment = analyze_sentiment(symbol)
    risk = calculate_risk(prices)

    score = calculate_score(prediction, sentiment)
    signal = generate_signal(prediction, sentiment)

    explanation = explain_reason(prediction, sentiment, risk, signal)

    return {
        "symbol": symbol,
        "prediction": prediction,
        "sentiment": sentiment,
        "risk": risk,
        "score": score,
        "signal": signal,
        "explanation": explanation
    }


def chatbot_reply(message: str):

    message_upper = message.upper()

    # =====================
    # GENERAL EDUCATION
    # =====================
    if "WHAT IS STOCK" in message_upper:
        return """
A stock represents ownership in a company.

When you buy stock:
• You own a percentage of that company
• You can earn profit if price rises
• Some stocks pay dividends

Stock prices move based on:
• Company performance
• News & sentiment
• Market demand & supply
• Economic conditions
"""

    if "WHY BUY" in message_upper:
        return """
You typically buy a stock when:

• Trend is upward
• News sentiment is positive
• Risk is manageable
• Company fundamentals are strong
• AI buy score is high

Buying without confirmation increases risk.
"""


    # =====================
    # ANALYZE SPECIFIC STOCK
    # =====================
    symbol = extract_valid_symbol(message_upper)

    if symbol:
        result = analyze_stock(symbol)

        if not result:
            return f"⚠️ Not enough data for {symbol}"

        return f"""
📊 {symbol} Analysis

Prediction: {round(result['prediction'],4)}
Sentiment Score: {round(result['sentiment'],3)}
Risk Level: {result['risk']}

Recommendation: {result['signal']}

{result['explanation']}
"""

    # =====================
    # BEST BUY
    # =====================
    if "BUY" in message_upper:

        results = []
        for sym in DEFAULT_STOCKS:
            try:
                res = analyze_stock(sym)
                if res:
                    results.append(res)
            except:
                pass

        if not results:
            return "Unable to analyze stocks right now."

        results.sort(key=lambda x: x["score"], reverse=True)
        best = results[0]

        return f"""
🔥 Strongest Buy Candidate Right Now:

👉 {best['symbol']}

Prediction: {round(best['prediction'],4)}
Sentiment: {round(best['sentiment'],3)}
Risk: {best['risk']}

Why?
{best['explanation']}
"""

    # =====================
    # SELL
    # =====================
    if "SELL" in message_upper:

        results = []
        for sym in DEFAULT_STOCKS:
            try:
                res = analyze_stock(sym)
                if res:
                    results.append(res)
            except:
                pass

        if not results:
            return "Unable to analyze stocks right now."

        results.sort(key=lambda x: x["score"])
        worst = results[0]

        return f"""
⚠️ Weakest Stock (Sell Consideration):

👉 {worst['symbol']}

Prediction: {round(worst['prediction'],4)}
Sentiment: {round(worst['sentiment'],3)}
Risk: {worst['risk']}

Why?
{worst['explanation']}
"""

    # =====================
    # MARKET / STRATEGY QUESTIONS
    # =====================
    if "LONG TERM" in message_upper:
        return """
Long-term investing focuses on:

• Strong companies
• Sustainable growth
• Low-to-moderate risk
• Compound returns over years

Short-term trading focuses on:

• Technical signals
• Volatility
• Momentum
• Quick gains
"""

    if "RISK" in message_upper:
        return """
Risk measures how volatile a stock is.

Low Risk:
• Stable price movement
• Lower returns but safer

High Risk:
• Large price swings
• Higher return potential
• Higher loss probability
"""

    return """
Try asking:

• Which stock should I buy right now?
• Which should I sell?
• Analyze TSLA
• Why should I buy AAPL?
• Explain stock market basics
"""