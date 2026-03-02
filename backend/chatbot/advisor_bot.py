import re
from data.fetch_prices import get_stock_data
from sentiment.sentiment_analyzer import analyze_sentiment
from ml.random_forest import predict_trend
from ml.risk_analyzer import calculate_risk


def chatbot_reply(message: str) -> str:

    message = message.upper()

    # Try detect stock symbol (simple detection)
    symbols = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN", "GOOGL"]

    for sym in symbols:
        if sym in message:
            prices = get_stock_data(sym)

            if not prices:
                return f"No data available for {sym}."

            prediction, _ = predict_trend(prices)
            sentiment = analyze_sentiment(sym)
            risk = calculate_risk(prices)

            if prediction > 0.005 and sentiment > 0:
                signal = "BUY"
            elif prediction < -0.005 and sentiment < 0:
                signal = "SELL"
            else:
                signal = "HOLD"

            return (
                f"📊 {sym} Analysis:\n\n"
                f"• Predicted Trend: {round(prediction,4)}\n"
                f"• Sentiment Score: {round(sentiment,3)}\n"
                f"• Risk Level: {risk}\n\n"
                f"👉 Current Recommendation: {signal}"
            )

    # If no symbol detected
    if "BEST STOCK" in message or "WHICH STOCK" in message:

        return (
            "I recommend checking the dashboard 🔥\n\n"
            "Look for stocks with:\n"
            "• BUY signal\n"
            "• Buy score above 70\n"
            "• Positive sentiment\n"
            "• Moderate/Low risk\n\n"
            "You can ask about a specific symbol like:\n"
            "👉 'Is TSLA a good buy?'"
        )

    return (
        "I can analyze specific stocks for you.\n"
        "Try asking:\n"
        "• 'Is AAPL a good buy?'\n"
        "• 'Should I sell TSLA?'\n"
        "• 'Risk level of NVDA?'\n"
    )