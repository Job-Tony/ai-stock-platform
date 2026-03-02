import re
from data.fetch_prices import get_stock_data
from sentiment.sentiment_analyzer import analyze_sentiment
from ml.random_forest import predict_trend
from ml.risk_analyzer import calculate_risk


def detect_symbol(message: str):
    """
    Try to detect stock ticker in message.
    Supports common US tickers (1–5 uppercase letters).
    """
    matches = re.findall(r"\b[A-Z]{1,5}\b", message.upper())
    if matches:
        return matches[0]
    return None


def generate_signal(prediction, sentiment):
    if prediction > 0.005 and sentiment > 0:
        return "BUY"
    elif prediction < -0.005 and sentiment < 0:
        return "SELL"
    else:
        return "HOLD"


def chatbot_reply(message: str) -> str:

    message = message.strip().upper()

    # Detect ticker
    symbol = detect_symbol(message)

    if symbol:

        prices = get_stock_data(symbol)

        if not prices:
            return f"❌ No data available for {symbol}. Try a valid ticker."

        prediction, _ = predict_trend(prices)
        sentiment = analyze_sentiment(symbol)
        risk = calculate_risk(prices)

        signal = generate_signal(prediction, sentiment)

        buy_score = int(((prediction * 0.7 + sentiment * 0.3) + 0.05) / 0.10 * 100)
        buy_score = max(0, min(100, buy_score))

        return f"""
📊 {symbol} Analysis

Prediction Trend: {round(prediction,4)}
Sentiment Score: {round(sentiment,3)}
Risk Level: {risk}
Buy Score: {buy_score}/100

👉 Recommendation: {signal}
        """

    # If asking which stock to buy
    if "WHICH STOCK" in message or "BEST STOCK" in message:

        top_candidates = ["AAPL", "MSFT", "TSLA", "NVDA"]

        best_symbol = None
        best_score = -1

        for sym in top_candidates:
            try:
                prices = get_stock_data(sym)
                prediction, _ = predict_trend(prices)
                sentiment = analyze_sentiment(sym)

                score = prediction * 0.7 + sentiment * 0.3

                if score > best_score:
                    best_score = score
                    best_symbol = sym
            except:
                continue

        if best_symbol:
            return f"""
🔥 Based on current AI analysis:

👉 {best_symbol} looks strongest right now.

Type:
• 'Analyze {best_symbol}'
to see full breakdown.
            """

        return "Unable to determine best stock right now."

    # Default fallback
    return """
I can analyze any stock for you 📈

Try:
• 'Is AAPL a good buy?'
• 'Analyze TSLA'
• 'Should I sell NVDA?'
• 'Risk level of MSFT?'
"""