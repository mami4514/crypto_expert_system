# app.py (ana uygulama dosyası)
import subprocess
import sys
import os
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import pandas as pd
import joblib

# Gereken paketler varsa otomatik yükle
REQUIRED_PACKAGES = ["flask", "requests", "pandas", "pandas-ta", "matplotlib", "joblib"]
for package in REQUIRED_PACKAGES:
    try:
        __import__(package.replace("-", "_"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Harici modüller
from binance_api import get_klines
from indicators import calculate_indicators, plot_indicators
from rules_engine import evaluate_rules

# Flask uygulaması
app = Flask(__name__)

# Modeli yükle
model = joblib.load("ml_model.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        symbols = request.form.getlist("symbols") or ["BTCUSDT"]
        risk = request.form.get("risk")
        term = request.form.get("term")

        for symbol in symbols:
            df = get_klines(symbol=symbol)
            df = calculate_indicators(df)
            latest = df.iloc[-1]

            rsi = latest["RSI"]
            macd = latest["MACD"]
            macd_signal = latest["MACD_signal"]

            advice = evaluate_rules(rsi, macd, macd_signal, risk, term)
            plot_path = plot_indicators(df, symbol)

            # ML tahmini
            input_features = pd.DataFrame([{
                "RSI": rsi,
                "MACD": macd,
                "MACD_signal": macd_signal
            }])
            prediction = model.predict(input_features)[0]

            if prediction == 1:
                ml_advice = "⚡ Model: AL sinyali verdi."
            elif prediction == -1:
                ml_advice = "⚠️ Model: SAT sinyali verdi."
            else:
                ml_advice = "🔄 Model: BEKLE öneriyor."

            results.append({
                "symbol": symbol,
                "rsi": rsi,
                "macd": macd,
                "macd_signal": macd_signal,
                "advice": advice,
                "plot": plot_path,
                "ml_advice": ml_advice
            })

    return render_template("index.html", result=results)

if __name__ == "__main__":
    app.run(debug=True)
