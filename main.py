import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np

from data import download_prices, prepare_series
from ratio import (
    compute_ratio,
    compute_bands,
    compute_rolling_zscore,
    current_percentile,
    compute_reversion_times,
    compute_forward_returns,
)


def plot_ratio(ax, ratio, bands):
    ax.plot(ratio.index, ratio.values, color="#2c3e50", linewidth=0.8, label="Ratio")
    ax.axhline(bands["mean"], color="#e74c3c", linewidth=1.2, linestyle="--", label="Mean")
    ax.axhline(bands["upper1"], color="#e67e22", linewidth=0.9, linestyle=":", label="±1 Std")
    ax.axhline(bands["lower1"], color="#e67e22", linewidth=0.9, linestyle=":")
    ax.axhline(bands["upper2"], color="#8e44ad", linewidth=0.9, linestyle=":", label="±2 Std")
    ax.axhline(bands["lower2"], color="#8e44ad", linewidth=0.9, linestyle=":")
    ax.fill_between(ratio.index, bands["lower1"], bands["upper1"], alpha=0.08, color="#e74c3c")
    ax.fill_between(ratio.index, bands["lower2"], bands["upper2"], alpha=0.05, color="#8e44ad")
    ax.set_title("Gold–Silver Ratio with Statistical Bands")
    ax.set_ylabel("Ratio")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)


def plot_histogram(ax, ratio, bands):
    current = ratio.iloc[-1]
    pct = current_percentile(ratio)

    ax.hist(ratio.values, bins=60, color="#2980b9", alpha=0.7, edgecolor="white", linewidth=0.3)
    ax.axvline(bands["mean"], color="#e74c3c", linewidth=1.2, linestyle="--", label=f"Mean ({bands['mean']:.1f})")
    ax.axvline(bands["upper1"], color="#e67e22", linewidth=0.9, linestyle=":")
    ax.axvline(bands["lower1"], color="#e67e22", linewidth=0.9, linestyle=":", label="±1 Std")
    ax.axvline(bands["upper2"], color="#8e44ad", linewidth=0.9, linestyle=":")
    ax.axvline(bands["lower2"], color="#8e44ad", linewidth=0.9, linestyle=":", label="±2 Std")
    ax.axvline(current, color="#27ae60", linewidth=1.4, linestyle="-", label=f"Current ({current:.1f}, {pct:.0f}th pct)")
    ax.set_title("Ratio Distribution")
    ax.set_xlabel("Ratio")
    ax.set_ylabel("Frequency")
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)


def plot_reversion(ax, ratio, bands):
    mean = bands["mean"]
    upper1 = bands["upper1"]
    horizon = 180

    events = []
    values = ratio.values
    i = 0
    while i < len(values) - horizon:
        if values[i] > upper1:
            events.append(values[i:i + horizon] - values[i])
            while i < len(values) and values[i] > upper1:
                i += 1
        else:
            i += 1

    if not events:
        ax.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes)
        return

    event_matrix = np.array(events)
    avg_path = event_matrix.mean(axis=0)
    std_path = event_matrix.std(axis=0)
    days = np.arange(horizon)

    ax.fill_between(days, avg_path - std_path, avg_path + std_path, color="#2980b9", alpha=0.2, label="±1 Std Dev")
    ax.plot(days, avg_path, color="#e74c3c", linewidth=2.0, label=f"Average path (n={len(events)})")
    ax.axhline(0, color="#2c3e50", linewidth=1.0, linestyle="--", label="Entry level (t=0)")
    ax.axhline(mean - upper1, color="#27ae60", linewidth=1.0, linestyle=":", label=f"Distance to mean ({mean - upper1:.1f})")
    ax.set_title("Gold–Silver Ratio Behavior After Extreme Deviations")
    ax.set_xlabel("Days After Extreme Ratio Event")
    ax.set_ylabel("Change in Ratio Since Event")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)


def plot_forward_returns(ax, fwd_results):
    horizons = [30, 60, 90]
    high_vals = [fwd_results["high"][h] * 100 for h in horizons]
    low_vals = [fwd_results["low"][h] * 100 for h in horizons]

    x = np.arange(len(horizons))
    width = 0.35

    bars1 = ax.bar(x - width / 2, high_vals, width, label="Ratio > +1σ (silver undervalued)", color="#e74c3c", alpha=0.8)
    bars2 = ax.bar(x + width / 2, low_vals, width, label="Ratio < −1σ (silver overvalued)", color="#27ae60", alpha=0.8)

    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(["30 days", "60 days", "90 days"])
    ax.set_ylabel("Avg Silver Return (%)")
    ax.set_title("Forward Silver Returns After Extreme Ratio Levels")
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3, axis="y")

    for bar in bars1:
        h = bar.get_height()
        va = "bottom" if h >= 0 else "top"
        ax.text(bar.get_x() + bar.get_width() / 2, h, f"{h:.1f}%", ha="center", va=va, fontsize=7)
    for bar in bars2:
        h = bar.get_height()
        va = "bottom" if h >= 0 else "top"
        ax.text(bar.get_x() + bar.get_width() / 2, h, f"{h:.1f}%", ha="center", va=va, fontsize=7)


def plot_summary_table(ax, ratio, bands, avg_days):
    ax.axis("off")
    current = ratio.iloc[-1]
    pct = current_percentile(ratio)

    rows = [
        ["Mean Ratio", f"{bands['mean']:.2f}"],
        ["Std Deviation", f"{bands['std']:.2f}"],
        ["Current Ratio", f"{current:.2f}"],
        ["Current Percentile", f"{pct:.1f}th"],
        ["+1σ Band", f"{bands['upper1']:.2f}"],
        ["−1σ Band", f"{bands['lower1']:.2f}"],
        ["+2σ Band", f"{bands['upper2']:.2f}"],
        ["−2σ Band", f"{bands['lower2']:.2f}"],
        ["Avg Reversion Time", f"{avg_days:.0f} days" if not np.isnan(avg_days) else "N/A"],
    ]

    table = ax.table(
        cellText=rows,
        colLabels=["Metric", "Value"],
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.7)

    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor("#2c3e50")
            cell.set_text_props(color="white", fontweight="bold")
        elif row % 2 == 0:
            cell.set_facecolor("#f2f2f2")
        cell.set_edgecolor("#cccccc")

    ax.set_title("Summary Statistics", fontweight="bold", pad=12)


def build_dashboard(df, ratio, bands, avg_days, reversion_days, fwd_results):
    fig = plt.figure(figsize=(16, 12), constrained_layout=True)
    fig.suptitle("Gold–Silver Ratio: Statistical Study", fontsize=14, fontweight="bold")

    gs = gridspec.GridSpec(3, 2, figure=fig)

    ax_ratio = fig.add_subplot(gs[0, :])
    ax_hist = fig.add_subplot(gs[1, 0])
    ax_rev = fig.add_subplot(gs[1, 1])
    ax_fwd = fig.add_subplot(gs[2, 0])
    ax_table = fig.add_subplot(gs[2, 1])

    plot_ratio(ax_ratio, ratio, bands)
    plot_histogram(ax_hist, ratio, bands)
    plot_reversion(ax_rev, ratio, bands)
    plot_forward_returns(ax_fwd, fwd_results)
    plot_summary_table(ax_table, ratio, bands, avg_days)

    plt.show()


def main():
    print("Downloading data...")
    gold_raw, silver_raw = download_prices()

    df = prepare_series(gold_raw, silver_raw)
    print(f"Data loaded: {df.index[0].date()} to {df.index[-1].date()}, {len(df)} trading days")

    ratio = compute_ratio(df)
    bands = compute_bands(ratio)

    print(f"Mean ratio: {bands['mean']:.2f}  |  Std: {bands['std']:.2f}")
    print(f"Current ratio: {ratio.iloc[-1]:.2f}  |  Percentile: {current_percentile(ratio):.1f}th")

    avg_days, reversion_days = compute_reversion_times(ratio, bands)
    print(f"Average reversion time: {avg_days:.0f} trading days ({len(reversion_days)} events)")

    fwd_results = compute_forward_returns(df, ratio, bands)
    print("\nForward silver returns after high ratio (ratio > +1σ):")
    for h, v in fwd_results["high"].items():
        print(f"  {h}d: {v:.2%}")
    print("Forward silver returns after low ratio (ratio < -1σ):")
    for h, v in fwd_results["low"].items():
        print(f"  {h}d: {v:.2%}")

    build_dashboard(df, ratio, bands, avg_days, reversion_days, fwd_results)


if __name__ == "__main__":
    main()