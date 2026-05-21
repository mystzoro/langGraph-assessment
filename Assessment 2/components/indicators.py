"""Technical indicator calculations."""

from __future__ import annotations

import numpy as np
import pandas as pd

from components.config import RSI_WINDOW, SMA_LONG_WINDOW, SMA_SHORT_WINDOW


def calculate_rsi(close_prices: pd.Series, window: int = RSI_WINDOW) -> pd.Series:
    """Calculate RSI using a rolling average approach."""

    delta = close_prices.diff()
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    average_gain = gains.rolling(window=window, min_periods=window).mean()
    average_loss = losses.rolling(window=window, min_periods=window).mean()

    relative_strength = pd.Series(np.where(average_loss == 0, np.nan, average_gain / average_loss), index=close_prices.index)
    rsi = 100 - (100 / (1 + relative_strength))

    rsi = rsi.where(~((average_gain == 0) & (average_loss == 0)), 50)
    rsi = rsi.where(~((average_gain > 0) & (average_loss == 0)), 100)
    return rsi.fillna(0)


def calculate_indicators(data: pd.DataFrame) -> dict[str, float]:
    """Calculate the technical indicators required by the project."""

    if data.empty:
        raise ValueError("Cannot calculate indicators from empty data.")

    if "Close" not in data.columns:
        raise ValueError("Input data must contain a Close column.")

    close_prices = data["Close"].astype(float)
    sma_10_series = close_prices.rolling(window=SMA_SHORT_WINDOW, min_periods=SMA_SHORT_WINDOW).mean()
    sma_20_series = close_prices.rolling(window=SMA_LONG_WINDOW, min_periods=SMA_LONG_WINDOW).mean()
    rsi_series = calculate_rsi(close_prices)

    if pd.isna(sma_10_series.iloc[-1]) or pd.isna(sma_20_series.iloc[-1]) or pd.isna(rsi_series.iloc[-1]):
        raise ValueError("Not enough data to calculate indicators.")

    return {
        "current_price": float(close_prices.iloc[-1]),
        "sma_10": float(sma_10_series.iloc[-1]),
        "sma_20": float(sma_20_series.iloc[-1]),
        "rsi_14": float(rsi_series.iloc[-1]),
    }
