# backend/trading/paper_trading.py

# Simple in-memory paper trading engine
# (resets when server restarts)

portfolio = {
    "balance": 100000.0,  # virtual cash
    "holdings": {}        # symbol -> quantity
}

def execute_trade(order: dict):
    """
    Execute a paper buy/sell trade.
    Order format:
    {
        "symbol": "AAPL",
        "action": "buy" | "sell",
        "quantity": 10,
        "price": 150
    }
    """
    symbol = order.get("symbol")
    action = order.get("action")
    quantity = int(order.get("quantity", 0))
    price = float(order.get("price", 0))

    if not symbol or action not in ("buy", "sell") or quantity <= 0 or price <= 0:
        return {"status": "error", "message": "Invalid order"}

    total = quantity * price

    if action == "buy":
        if portfolio["balance"] < total:
            return {"status": "error", "message": "Insufficient balance"}

        portfolio["balance"] -= total
        portfolio["holdings"][symbol] = portfolio["holdings"].get(symbol, 0) + quantity

    else:  # sell
        if portfolio["holdings"].get(symbol, 0) < quantity:
            return {"status": "error", "message": "Insufficient holdings"}

        portfolio["holdings"][symbol] -= quantity
        portfolio["balance"] += total

    return {
        "status": "success",
        "portfolio": portfolio
    }
