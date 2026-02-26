NAME_TO_CODE = {
    "トヨタ": "7203",
    "フジプレアム": "4237",
    "日本精密": "7771",
    "山一電機": "6941",
    "ヒーハイスト": "6433",
    "アドウェイズ": "2489",
    "アスカネット": "2438",
    "有沢製作所": "5208"
}
from fastapi import FastAPI
import yfinance as yf
import pandas as pd
import ta

app = FastAPI()

def get_stock_data(code):

    ticker = f"{code}.T"
    df = yf.download(ticker, period="3mo", interval="1d")

    if df.empty:
        return {"error": "データ取得失敗"}

    df["RSI"] = ta.momentum.RSIIndicator(
        close=df["Close"], window=14
    ).rsi()

    latest = df.iloc[-1]

    return {
        "code": code,
        "price": float(latest["Close"]),
        "volume": int(latest["Volume"]),
        "RSI": round(float(latest["RSI"]), 2)
    }

@app.get("/stock/{name}")
def stock(name: str):

    code = NAME_TO_CODE.get(name, name)

    return get_stock_data(code)
