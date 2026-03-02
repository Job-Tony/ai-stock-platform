from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from data.fetch_news import fetch_news

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(symbol: str) -> float:
    """
    Returns sentiment score between -1 and +1.
    Handles indices & commodities safely.
    Combines VADER + API sentiment.
    """

    try:
        symbol = symbol.upper()

        # Indices & commodities → neutral baseline
        if symbol.startswith("^") or symbol in ["GC=F", "SI=F"]:
            return 0.0

        news_data = fetch_news(symbol)

        headlines = news_data.get("headlines", [])
        api_sentiment = float(news_data.get("sentiment", 0.0))

        if not headlines:
            return 0.0

        vader_scores = []

        for text in headlines:
            score = analyzer.polarity_scores(text)["compound"]

            if abs(score) >= 0.05:
                vader_scores.append(score)

        if not vader_scores:
            return 0.0

        vader_avg = sum(vader_scores) / len(vader_scores)

        # Stronger weight to VADER since API sentiment is 0
        combined = (vader_avg * 0.75) + (api_sentiment * 0.25)

        combined = max(-1.0, min(1.0, combined))

        return round(combined, 3)

    except Exception:
        return 0.0