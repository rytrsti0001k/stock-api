from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def test():
    return f"API_KEY={os.environ.get('FINNHUB_API_KEY')}"
