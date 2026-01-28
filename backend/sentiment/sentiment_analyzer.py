from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from data.fetch_news import get_news

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(symbol: str) -> float:
    news = get_news(symbol)

    if not news:
        return 0.0

    scores = [analyzer.polarity_scores(text)["compound"] for text in news]
    return round(sum(scores) / len(scores), 2)
