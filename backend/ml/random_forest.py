import numpy as np
from sklearn.ensemble import RandomForestRegressor


def predict_trend(price_data):
    """
    Predict short-term stock trend using Random Forest
    Returns normalized trend between -1 and +1
    """

    if not price_data or len(price_data) < 10:
        return 0.0

    try:
        # Extract closing prices from list of dicts
        closes = np.array([day["Close"] for day in price_data], dtype=float)

        # Features: previous day's close
        X = closes[:-1].reshape(-1, 1)
        y = closes[1:]

        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

        model.fit(X, y)

        prediction = model.predict([[closes[-1]]])[0]

        # Trend score
        trend = (prediction - closes[-1]) / closes[-1]

        return round(float(trend), 4)

    except Exception as e:
        print("ML prediction error:", e)
        return 0.0