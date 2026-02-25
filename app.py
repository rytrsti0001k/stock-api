from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("TWELVE_API_KEY")

@app.route("/stock/<symbol>")
def get_stock(symbol):

    symbol_t = f"{symbol}.JP"

    price_url = f"https://api.twelvedata.com/price?symbol={symbol_t}&apikey={API_KEY}"
    price_res = requests.get(price_url).json()

    rsi_url = f"https://api.twelvedata.com/rsi?symbol={symbol_t}&interval=1day&time_period=14&apikey={API_KEY}"
    rsi_res = requests.get(rsi_url).json()

    if "price" not in price_res or "values" not in rsi_res:
        return jsonify({"error": "API error", "price": price_res, "rsi": rsi_res}), 400

    return jsonify({
        "price": float(price_res["price"]),
        "RSI": float(rsi_res["values"][0]["rsi"])
    })
