Gold–Silver Ratio: Statistical Study
Overview

This project studies the historical behavior of the gold–silver ratio and how the relationship between the two metals evolves after extreme deviations from its long-term average.

Rather than building a trading strategy, the goal is to understand the statistical structure of the ratio itself. The analysis focuses on how frequently extreme ratios occur, how long they persist, and how silver performs following these events.

Gold and silver often move together because they are both precious metals and respond to similar macroeconomic forces such as inflation expectations, interest rates, and safe-haven demand. However, silver also has significant industrial demand, which can cause the relative pricing between the two metals to diverge.

This project investigates whether those divergences tend to correct over time.

Research Questions

The analysis explores three main questions:

How is the gold–silver ratio distributed historically?

When the ratio moves far from its long-term average, how does it behave afterward?

Do extreme ratios predict future silver performance?

Data

Assets: Gold Futures (GC=F) and Silver Futures (SI=F)

Source: Yahoo Finance via yfinance

Frequency: Daily data

Sample period: 2010 – present

The gold–silver ratio is calculated as:

Gold Price / Silver Price

Methodology
Ratio Statistics

The long-term mean and standard deviation of the ratio are calculated to identify statistically extreme levels.

Two deviation thresholds are examined:

Mean ± 1 standard deviation

Mean ± 2 standard deviations

These bands help identify periods where the relative pricing between gold and silver becomes unusually stretched.

Ratio Distribution

A histogram of the ratio is constructed to examine how frequently different levels occur. This provides context for understanding whether the current ratio sits in a historically common or rare range.

Event Study

To analyze mean reversion behavior, the study identifies periods when the ratio exceeds one standard deviation above its historical mean.

Each event is aligned at the moment the extreme occurs (t = 0), and the ratio is tracked for the following 180 trading days.

This allows us to observe the average path of the ratio after extreme deviations and evaluate whether it tends to drift back toward its long-term equilibrium.

Forward Silver Returns

The study also measures how silver performs after extreme ratio levels.

When the ratio exceeds +1 standard deviation, silver is relatively cheap compared to gold.
When the ratio falls below −1 standard deviation, silver is relatively expensive.

Average forward silver returns are measured over:

30 trading days

60 trading days

90 trading days

This helps evaluate whether extreme ratios provide predictive information about relative performance.

Key Observations

Several patterns emerge from the analysis:

The long-term average gold–silver ratio is approximately 73.

Extreme deviations from this level occur periodically but are relatively rare.

Mean reversion tends to be slow and noisy, often taking months or years rather than weeks.

When the ratio rises significantly above its historical average, silver has historically produced stronger forward returns.

These results suggest that the ratio contains useful information about relative valuation, but the adjustment process is gradual and unpredictable.

Project Structure
main.py
data.py
ratio.py
analysis.py
metrics.py
README.md

The project is written entirely in Python using:

pandas

numpy

matplotlib

yfinance

Conclusion

The gold–silver ratio offers insight into the relative valuation of the two metals, but extreme deviations do not necessarily revert quickly. Historical data suggests that mean reversion can be slow and uneven, which helps explain why simple spread-trading strategies often struggle.

A more robust approach would likely combine ratio analysis with additional signals such as momentum, macroeconomic variables, or market volatility.