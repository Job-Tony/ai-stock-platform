from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from backend.data.fetch_news import fetch_news

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(symbol: str) -> float:
    """
    Returns sentiment score between -1 and +1
    Combines Alpha Vantage news + VADER sentiment analysis
    """

    try:
        news_data = fetch_news(symbol)

        headlines = news_data.get("headlines", [])
        av_sentiment = news_data.get("sentiment", 0.0)

        if not headlines:
            return av_sentiment

        vader_scores = [
            analyzer.polarity_scores(text)["compound"]
            for text in headlines
        ]

        vader_avg = sum(vader_scores) / len(vader_scores)

        # 🔥 Combine Alpha Vantage sentiment + NLP sentiment
        combined_sentiment = (vader_avg * 0.6) + (av_sentiment * 0.4)

        return round(combined_sentiment, 3)

    except Exception:
        return 0.0
