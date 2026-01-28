import numpy as np
from sklearn.ensemble import RandomForestRegressor

def predict_trend(price_data):
    """
    Predict short-term stock trend using Random Forest
    Returns a value between -1 and +1
    """
    if not price_data or len(price_data) < 10:
        return 0.0

    # Extract closing prices
    closes = np.array(price_data)

    # Feature: previous day prices
    X = closes[:-1].reshape(-1, 1)
    y = closes[1:]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    prediction = model.predict([[closes[-1]]])[0]

    # Normalize to a trend score
    trend = (prediction - closes[-1]) / closes[-1]

    return round(float(trend), 4)
