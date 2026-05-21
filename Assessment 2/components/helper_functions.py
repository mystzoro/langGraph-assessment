"""Helper functions for validation, fetching, and reporting."""

from __future__ import annotations

import re
from typing import Any

import pandas as pd
import yfinance as yf

from components.config import MIN_HISTORY_DAYS, RECOMMENDATION_BUY, RECOMMENDATION_HOLD, RECOMMENDATION_SELL


TICKER_PATTERN = re.compile(r"^[A-Z][A-Z0-9\.-]{0,9}$")


def validate_ticker_symbol(ticker_symbol: str) -> str:
    """Validate and normalize a ticker symbol."""

    normalized = ticker_symbol.strip().upper()
    if not normalized:
        raise ValueError("Ticker symbol cannot be empty.")

    if not TICKER_PATTERN.fullmatch(normalized):
        raise ValueError(f"Invalid ticker symbol: {ticker_symbol!r}")

    return normalized


def fetch_stock_history(ticker_symbol: str) -> pd.DataFrame:
    """Fetch historical stock data for the last 60 days."""

    ticker = yf.Ticker(ticker_symbol)
    try:
        history = ticker.history(period=f"{MIN_HISTORY_DAYS}d", interval="1d")
    except Exception as exc:  # noqa: BLE001 - surfaced as a domain error
        raise RuntimeError(f"Failed to fetch data for {ticker_symbol}: {exc}") from exc

    if history is None or history.empty:
        raise ValueError(f"No historical data returned for ticker {ticker_symbol}.")

    required_columns = {"Close"}
    missing_columns = required_columns.difference(history.columns)
    if missing_columns:
        raise ValueError(
            f"Historical data for {ticker_symbol} is missing required columns: {sorted(missing_columns)}"
        )

    return history.copy()


def derive_recommendation(sma_10: float, sma_20: float, rsi_14: float) -> tuple[str, str]:
    """Return the recommendation and explanation from indicator values."""

    if sma_10 > sma_20 and rsi_14 < 70:
        return (
            RECOMMENDATION_BUY,
            "Short-term momentum is stronger than long-term momentum and RSI is within acceptable range.",
        )

    if sma_10 < sma_20 and rsi_14 > 30:
        return (
            RECOMMENDATION_SELL,
            "Short-term momentum is weaker than long-term momentum and RSI suggests the move is not oversold.",
        )

    return (
        RECOMMENDATION_HOLD,
        "Momentum and RSI signals do not provide a clear directional edge.",
    )


def format_currency(value: Any) -> str:
    """Format a numeric value as a currency string."""

    if pd.isna(value):
        return "N/A"
    return f"${float(value):,.2f}"


def format_numeric(value: Any) -> str:
    """Format a numeric value for display."""

    if pd.isna(value):
        return "N/A"
    return f"{float(value):.2f}"


def print_report(report: str) -> None:
    """Print the analysis report cleanly."""

    print(report)
