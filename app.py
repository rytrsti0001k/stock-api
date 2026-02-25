from flask import Flask, jsonify
import requests
import pandas as pd

app = Flask(__name__)

API_KEY = "YOUR_API_KEY"

def calculate_rsi(close_prices, period=14):
    delta = pd.Series(close_prices).diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi.iloc[-1], 2)

@app.route("/stock/<symbol>")
def get_stock(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}.T&apikey={API_KEY}"
    data = requests.get(url).json()

    series = data["Time Series (Daily)"]
    dates = list(series.keys())
    closes = [float(series[d]["4. close"]) for d in dates[:20]]

    latest_close = closes[0]
    latest_volume = series[dates[0]]["5. volume"]
    rsi = calculate_rsi(closes)

    return jsonify({
        "price": latest_close,
        "volume": latest_volume,
        "RSI": rsi
    })
