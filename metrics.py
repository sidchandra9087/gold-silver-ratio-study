import numpy as np
import pandas as pd


def annualized_return(returns):
    total = (1 + returns).prod()
    n_years = len(returns) / 252
    return total ** (1 / n_years) - 1


def annualized_volatility(returns):
    return returns.std() * np.sqrt(252)


def sharpe_ratio(returns, rf=0.0):
    excess = returns - rf / 252
    if excess.std() == 0:
        return 0.0
    return (excess.mean() / excess.std()) * np.sqrt(252)


def compute_drawdown(returns):
    cumulative = (1 + returns).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    return drawdown


def max_drawdown(returns):
    return compute_drawdown(returns).min()


def calmar_ratio(returns):
    ann_ret = annualized_return(returns)
    md = abs(max_drawdown(returns))
    if md == 0:
        return 0.0
    return ann_ret / md


def rolling_sharpe(returns, window=60):
    def sharpe_window(x):
        if x.std() == 0:
            return 0.0
        return (x.mean() / x.std()) * np.sqrt(252)

    return returns.rolling(window).apply(sharpe_window, raw=True)


def summary_metrics(returns, label):
    return {
        "label": label,
        "ann_return": annualized_return(returns),
        "ann_vol": annualized_volatility(returns),
        "sharpe": sharpe_ratio(returns),
        "max_dd": max_drawdown(returns),
        "calmar": calmar_ratio(returns),
    }