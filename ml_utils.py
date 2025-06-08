import requests
import json
import pandas as pd
import pandas_ta as ta
from datetime import datetime
import ssl
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

class SSLAdapter(HTTPAdapter):
    def __init__(self, ssl_version=None, **kwargs):
        self.ssl_context = create_urllib3_context(ssl_version=ssl_version)
        self.ssl_context.check_hostname = False  # Disable hostname checking
        self.ssl_context.verify_mode = ssl.CERT_NONE  # Disable SSL verification
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().proxy_manager_for(*args, **kwargs)

def get_klines(symbol="BTCUSDT", interval="1h", limit=500):
    session = requests.Session()
    session.mount("http://", SSLAdapter())

    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = session.get(url, verify=False)  # SSL verification disabled

    if response.status_code != 200:
        raise Exception(f"Binance API hata verdi: {response.status_code} - {response.reason}")

    data = response.json()
    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["close"] = df["close"].astype(float)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    return df[["open_time", "close"]]

def prepare_ml_dataset(symbol="BTCUSDT"):
    df = get_klines(symbol, interval="1h", limit=500)
    df['RSI'] = ta.rsi(df['close'], length=14)
    macd = ta.macd(df['close'])
    df['MACD'] = macd['MACD_12_26_9']
    df['MACD_signal'] = macd['MACDs_12_26_9']

    df["future_price"] = df["close"].shift(-1)
    df["price_change"] = (df["future_price"] - df["close"]) / df["close"]

    def label(row):
        if row["price_change"] > 0.01:
            return 1
        elif row["price_change"] < -0.01:
            return -1
        else:
            return 0

    df["label"] = df.apply(label, axis=1)
    df.dropna(inplace=True)

    features = df[["RSI", "MACD", "MACD_signal"]]
    labels = df["label"]

    return features, labels
