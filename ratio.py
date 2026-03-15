import pandas as pd
import numpy as np
from scipy import stats as scipy_stats


def compute_ratio(df):
    return df["gold"] / df["silver"]


def compute_bands(ratio):
    mean = ratio.mean()
    std = ratio.std()

    bands = {
        "mean": mean,
        "std": std,
        "upper1": mean + std,
        "lower1": mean - std,
        "upper2": mean + 2 * std,
        "lower2": mean - 2 * std,
    }
    return bands


def compute_rolling_zscore(ratio, window=252):
    rolling_mean = ratio.rolling(window).mean()
    rolling_std = ratio.rolling(window).std()
    return (ratio - rolling_mean) / rolling_std


def current_percentile(ratio):
    latest = ratio.iloc[-1]
    return scipy_stats.percentileofscore(ratio.dropna(), latest)


def compute_reversion_times(ratio, bands):
    mean = bands["mean"]
    upper1 = bands["upper1"]
    lower1 = bands["lower1"]

    reversion_days = []
    i = 0
    values = ratio.values

    while i < len(values):
        if values[i] > upper1 or values[i] < lower1:
            start = i
            crossed_mean = False
            j = i + 1
            while j < len(values):
                if values[i] > upper1 and values[j] <= mean:
                    crossed_mean = True
                    break
                if values[i] < lower1 and values[j] >= mean:
                    crossed_mean = True
                    break
                j += 1
            if crossed_mean:
                reversion_days.append(j - start)
            i = j + 1
        else:
            i += 1

    avg_days = np.mean(reversion_days) if reversion_days else np.nan
    return avg_days, reversion_days


def compute_forward_returns(df, ratio, bands, horizons=(30, 60, 90)):
    silver_ret = df["silver"].pct_change()
    results = {"high": {}, "low": {}}

    for h in horizons:
        fwd = silver_ret.rolling(h).sum().shift(-h)
        high_mask = ratio > bands["upper1"]
        low_mask = ratio < bands["lower1"]
        results["high"][h] = fwd[high_mask].mean()
        results["low"][h] = fwd[low_mask].mean()

    return results