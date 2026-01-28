# backend/chatbot/advisor_bot.py

def chatbot_reply(message: str) -> str:
    """
    Simple rule-based investment advisor chatbot
    """
    message = message.lower()

    if "buy" in message:
        return "Consider buying fundamentally strong stocks when sentiment and trend are positive."
    elif "sell" in message:
        return "You may consider selling if sentiment turns negative or the trend weakens."
    elif "best stock" in message:
        return "Based on current analysis, stocks with high buy scores are better options."
    elif "risk" in message:
        return "Diversification and proper risk management are key to long-term success."
    else:
        return "Ask me about buying, selling, trends, or stock recommendations."
