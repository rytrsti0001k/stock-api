from flask import Flask, jsonify
import yfinance as yf
import pandas as pd

app = Flask(__name__)

# RSI計算
def calculate_rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

@app.route("/")
def home():
    return "Stock API running"

@app.route("/stock/<symbol>")
def get_stock(symbol):

    ticker = yf.Ticker(f"{symbol}.T")
    hist = ticker.history(period="1mo")

    if hist.empty:
        return jsonify({"error": "No stock data"}), 404

    price = hist["Close"].iloc[-1]
    volume = hist["Volume"].iloc[-1]

    rsi_series = calculate_rsi(hist["Close"])
    rsi = round(rsi_series.iloc[-1], 2)

    return jsonify({
        "symbol": symbol,
        "price": round(float(price), 2),
        "volume": int(volume),
        "RSI": rsi
    })
