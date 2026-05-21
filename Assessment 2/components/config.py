"""Configuration for the stock analysis agent."""

from __future__ import annotations

MIN_HISTORY_DAYS = 60
SMA_SHORT_WINDOW = 10
SMA_LONG_WINDOW = 20
RSI_WINDOW = 14

RECOMMENDATION_BUY = "BUY"
RECOMMENDATION_HOLD = "HOLD"
RECOMMENDATION_SELL = "SELL"
