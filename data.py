import yfinance as yf
import pandas as pd


def download_prices(start="2010-01-01", end=None):
    gold = yf.download("GC=F", start=start, end=end, auto_adjust=True)
    silver = yf.download("SI=F", start=start, end=end, auto_adjust=True)
    return gold, silver


def prepare_series(gold, silver):
    gold_close = gold["Close"].squeeze()
    silver_close = silver["Close"].squeeze()

    df = pd.DataFrame({"gold": gold_close, "silver": silver_close})
    df = df.dropna()
    return df