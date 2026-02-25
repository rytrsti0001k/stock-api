from flask import Flask, jsonify
import requests
import pandas as pd
import os
import time

app = Flask(__name__)

API_KEY = os.environ.get("FINNHUB_API_KEY")

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
    symbol_t = f"{symbol}.T"

    # 現在時刻
    to_time = int(time.time())
    from_time = to_time - (60 * 60 * 24 * 40)  # 約40日分

    # 最新株価
    quote_url = f"https://finnhub.io/api/v1/quote?symbol={symbol_t}&token={API_KEY}"
    quote = requests.get(quote_url).json()

    # 過去データ（RSI用）
    candle_url = f"https://finnhub.io/api/v1/stock/candle?symbol={symbol_t}&resolution=D&from={from_time}&to={to_time}&token={API_KEY}"
    candle = requests.get(candle_url).json()

    if "c" not in quote or candle.get("s") != "ok":
        return jsonify({"error": "Finnhub API error", "quote": quote, "candle": candle}), 400

    closes = candle["c"]
    rsi = calculate_rsi(closes)

    return jsonify({
        "price": quote["c"],
        "volume": quote["v"],
        "RSI": rsi
    })
