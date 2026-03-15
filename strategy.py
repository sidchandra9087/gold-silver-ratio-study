import numpy as np
import pandas as pd


def compute_signal(ratio, bands):
    signal = pd.Series(0, index=ratio.index)
    signal[ratio > bands["upper1"]] = -1
    signal[ratio < bands["lower1"]] = 1
    return signal


def compute_returns(df, signal):
    gold_ret = df["gold"].pct_change()
    silver_ret = df["silver"].pct_change()

    spread = silver_ret - gold_ret

    shifted_signal = signal.shift(1)
    strategy_ret = shifted_signal * spread

    benchmark_ret = silver_ret

    return strategy_ret.dropna(), benchmark_ret.dropna()