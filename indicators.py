import pandas_ta as ta
import matplotlib.pyplot as plt
import os

def calculate_indicators(df):
    df['RSI'] = ta.rsi(df['close'], length=14)
    macd = ta.macd(df['close'])
    df['MACD'] = macd['MACD_12_26_9']
    df['MACD_signal'] = macd['MACDs_12_26_9']
    return df

def plot_indicators(df, symbol):
    plt.figure(figsize=(10, 5))
    plt.plot(df["open_time"], df["RSI"], label="RSI")
    plt.plot(df["open_time"], df["MACD"], label="MACD")
    plt.plot(df["open_time"], df["MACD_signal"], label="MACD Signal")
    plt.legend()
    plt.title(f"{symbol} RSI & MACD")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plot_path = f"static/plots/{symbol}.png"
    os.makedirs("static/plots", exist_ok=True)
    plt.savefig(plot_path)
    plt.close()
    return plot_path
