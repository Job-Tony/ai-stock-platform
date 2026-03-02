import re
from data.fetch_prices import get_stock_data
from sentiment.sentiment_analyzer import analyze_sentiment
from ml.random_forest import predict_trend
from ml.risk_analyzer import calculate_risk

# ===============================
# GLOBAL STOCK LIST
# ===============================

DEFAULT_STOCKS = [

    # 🇺🇸 US Tech
    "AAPL", "MSFT", "TSLA", "NVDA", "AMZN", "GOOGL",
    "META", "NFLX",

    # 🇺🇸 Blue-chip
    "JPM", "V", "WMT", "KO",

    # 🇺🇸 ETFs
    "SPY", "QQQ",

    # 🇮🇳 Indian Stocks
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "ITC.NS",

    # 🇮🇳 Indices
    "^NSEI",      # NIFTY 50
    "^BSESN",     # SENSEX

    # 🪙 Commodities
    "GC=F",       # Gold
    "SI=F",       # Silver
]


# ===============================
# SAFE SYMBOL EXTRACTION
# ===============================

def extract_symbol(message: str):
    msg = message.upper()
    for sym in DEFAULT_STOCKS:
        if sym in msg:
            return sym
    return None


# ===============================
# SIGNAL LOGIC
# ===============================

def generate_signal(prediction, sentiment):
    if prediction > 0.005 and sentiment > 0:
        return "BUY"
    elif prediction < -0.005 and sentiment < 0:
        return "SELL"
    else:
        return "HOLD"


# ===============================
# STOCK ANALYSIS
# ===============================

def explain_stock(symbol):

    prices = get_stock_data(symbol)

    if not prices or len(prices) < 20:
        return f"⚠ Not enough data available for {symbol}. Try another ticker."

    prediction, _ = predict_trend(prices)
    sentiment = analyze_sentiment(symbol)
    risk = calculate_risk(prices)

    signal = generate_signal(prediction, sentiment)

    return f"""
📊 Detailed AI Analysis for {symbol}

Trend Prediction: {round(prediction,4)}
News Sentiment: {round(sentiment,3)}
Risk Level: {risk}

Explanation:
• Trend indicates {'upward strength' if prediction > 0 else 'downward pressure'}.
• Sentiment shows {'positive' if sentiment > 0 else 'negative' if sentiment < 0 else 'neutral'} tone.
• Risk measures volatility behavior.

Final AI Recommendation → {signal}

Decision based on Machine Learning + NLP Sentiment + Risk Modeling.
"""


# ===============================
# RANK ALL STOCKS
# ===============================

def compare_stocks():

    results = []

    for sym in DEFAULT_STOCKS:
        try:
            prices = get_stock_data(sym)
            if not prices or len(prices) < 20:
                continue

            prediction, _ = predict_trend(prices)
            sentiment = analyze_sentiment(sym)

            score = prediction * 0.7 + sentiment * 0.3
            results.append((sym, score))

        except:
            continue

    if not results:
        return "⚠ Unable to analyze market currently."

    results.sort(key=lambda x: x[1], reverse=True)

    best = results[0]
    worst = results[-1]

    return f"""
📈 Global Market Ranking

🔥 Strongest Asset: {best[0]}
⚠ Weakest Asset: {worst[0]}

Ranking calculated using trend + sentiment scoring model.
"""


# ===============================
# CHATBOT MAIN
# ===============================

def chatbot_reply(message: str):

    msg = message.upper()

    if "WHAT IS STOCK" in msg:
        return """
A stock represents ownership in a company.

When you buy stock:
• You own part of the business
• You benefit from growth
• You may receive dividends

Stock prices move based on performance, news, and investor demand.
"""

    if "RISK" in msg:
        return """
Risk measures volatility.

Low Risk → Stable movement
High Risk → Large price swings

Higher risk can mean higher returns but higher losses.
"""

    if "HOW MARKET WORK" in msg:
        return """
Markets operate on demand and supply.

Price rises → More buyers
Price falls → More sellers

Markets react to earnings, news, interest rates, and global events.
"""

    symbol = extract_symbol(msg)
    if symbol:
        return explain_stock(symbol)

    if "BUY" in msg or "BEST" in msg or "WHICH" in msg:
        return compare_stocks()

    if "SELL" in msg:
        return compare_stocks()

    return "Ask me to analyze AAPL, RELIANCE.NS, GC=F, ^BSESN or compare stocks."