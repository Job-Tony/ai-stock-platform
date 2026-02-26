from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from data.fetch_news import fetch_news

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(symbol: str) -> float:
    """
    Returns sentiment score between -1 and +1
    Combines VADER + API sentiment
    Filters neutral noise
    """

    try:
        news_data = fetch_news(symbol)

        headlines = news_data.get("headlines", [])
        api_sentiment = float(news_data.get("sentiment", 0.0))

        if not headlines:
            return round(api_sentiment, 3)

        vader_scores = []

        for text in headlines:
            score = analyzer.polarity_scores(text)["compound"]

            # Filter weak neutral noise
            if abs(score) >= 0.05:
                vader_scores.append(score)

        if not vader_scores:
            vader_avg = 0.0
        else:
            vader_avg = sum(vader_scores) / len(vader_scores)

        # Weighted fusion
        combined = (vader_avg * 0.65) + (api_sentiment * 0.35)

        # Clamp range safely
        combined = max(-1.0, min(1.0, combined))

        return round(combined, 3)

    except Exception as e:
        print("Sentiment error:", e)
        return 0.0