# backend/chatbot/advisor_bot.py

def chatbot_reply(message: str) -> str:
    """
    Context-aware AI stock advisor chatbot (rule-based, expandable)
    """

    msg = message.lower()

    # BUY / SELL
    if "buy" in msg:
        return (
            "Buying a stock is generally considered when:\n"
            "• Trend is upward\n"
            "• Sentiment is positive\n"
            "• Buy score is high\n\n"
            "Check the dashboard for AI-based confirmation before deciding."
        )

    if "sell" in msg:
        return (
            "Selling may be considered when:\n"
            "• Trend weakens\n"
            "• Sentiment turns negative\n"
            "• Price hits resistance or target\n\n"
            "Risk management is more important than profit."
        )

    # RISK
    if "risk" in msg or "safe" in msg:
        return (
            "All stocks carry risk. To reduce it:\n"
            "• Diversify across sectors\n"
            "• Avoid overexposure to a single stock\n"
            "• Use stop-losses\n"
            "• Don’t invest money you can’t afford to lose"
        )

    # LONG TERM
    if "long term" in msg or "invest" in msg:
        return (
            "For long-term investing:\n"
            "• Focus on strong fundamentals\n"
            "• Ignore short-term noise\n"
            "• Review quarterly performance\n"
            "• Stay consistent and patient"
        )

    # SHORT TERM / TRADING
    if "short term" in msg or "trading" in msg:
        return (
            "Short-term trading relies on:\n"
            "• Momentum\n"
            "• Volume\n"
            "• Sentiment shifts\n"
            "• Technical indicators\n\n"
            "Paper trade first before risking capital."
        )

    # BEST STOCK
    if "best stock" in msg or "recommend" in msg:
        return (
            "I can’t name a single 'best' stock, but you can:\n"
            "• Use the dashboard to compare buy scores\n"
            "• Look for strong trend + sentiment\n"
            "• Avoid hype-driven decisions"
        )

    # DEFAULT SMART RESPONSE
    return (
        "I can help you with:\n"
        "• Buy / Sell decisions\n"
        "• Risk management\n"
        "• Long-term vs short-term strategy\n"
        "• Market behavior\n\n"
        "Try asking something more specific 🙂"
    )
