"""LangGraph nodes for stock analysis."""

from __future__ import annotations

from typing import cast

import pandas as pd

from components.helper_functions import (
    derive_recommendation,
    fetch_stock_history,
    format_currency,
    format_numeric,
    validate_ticker_symbol,
)
from components.config import MIN_HISTORY_DAYS, RSI_WINDOW, SMA_LONG_WINDOW, SMA_SHORT_WINDOW
from components.indicators import calculate_indicators


def _format_history_window(stock_data: pd.DataFrame) -> str:
    """Return a readable date range for the fetched history."""

    if stock_data.empty:
        return "N/A"

    start_date = pd.to_datetime(stock_data.index.min()).date()
    end_date = pd.to_datetime(stock_data.index.max()).date()
    return f"{start_date} to {end_date}"


def _format_price_change(stock_data: pd.DataFrame) -> str:
    """Return the absolute and percentage change across the fetched history."""

    close_series = stock_data.get("Close")
    if close_series is None or close_series.empty:
        return "N/A"

    first_close = float(close_series.iloc[0])
    last_close = float(close_series.iloc[-1])
    absolute_change = last_close - first_close
    percentage_change = (absolute_change / first_close) * 100 if first_close else 0.0
    return f"{format_currency(absolute_change)} ({percentage_change:+.2f}%)"


def fetch_stock_data_node(state: dict) -> dict:
    """Fetch and validate stock data."""

    if state.get("error"):
        return state

    ticker_symbol = state.get("ticker_symbol", "")
    try:
        normalized_symbol = validate_ticker_symbol(ticker_symbol)
        stock_data = fetch_stock_history(normalized_symbol)
        return {
            **state,
            "ticker_symbol": normalized_symbol,
            "ticker_validation": f"Passed: normalized to {normalized_symbol}",
            "stock_data": stock_data,
        }
    except Exception as exc:  # noqa: BLE001 - converted to workflow state
        return {**state, "ticker_validation": f"Failed: {exc}", "error": str(exc)}


def calculate_indicators_node(state: dict) -> dict:
    """Calculate the required technical indicators."""

    if state.get("error"):
        return state

    stock_data = state.get("stock_data")
    if not isinstance(stock_data, pd.DataFrame):
        return {**state, "error": "Stock data is unavailable or invalid."}

    try:
        indicators = calculate_indicators(stock_data)
        return {**state, "indicators": indicators}
    except Exception as exc:  # noqa: BLE001 - converted to workflow state
        return {**state, "error": str(exc)}


def generate_recommendation_node(state: dict) -> dict:
    """Generate a BUY, HOLD, or SELL recommendation."""

    if state.get("error"):
        return state

    indicators = state.get("indicators") or {}
    try:
        recommendation, reason = derive_recommendation(
            float(indicators["sma_10"]),
            float(indicators["sma_20"]),
            float(indicators["rsi_14"]),
        )
        return {**state, "recommendation": recommendation, "reason": reason}
    except Exception as exc:  # noqa: BLE001 - converted to workflow state
        return {**state, "error": str(exc)}


def format_analysis_report_node(state: dict) -> dict:
    """Format the final report for display."""

    ticker_symbol = state.get("ticker_symbol", "N/A")
    ticker_validation = state.get("ticker_validation", "Not recorded")
    indicators = cast(dict[str, float], state.get("indicators") or {})
    stock_data = state.get("stock_data")

    if state.get("error"):
        report = "\n".join(
            [
                "==================================",
                "STOCK MARKET ANALYSIS REPORT",
                "==================================",
                "",
                f"Stock Symbol: {ticker_symbol}",
                f"Ticker Validation: {ticker_validation}",
                "",
                f"Error: {state['error']}",
                "",
                "==================================",
            ]
        )
        return {**state, "report": report}

    report = "\n".join(
        [
            "==================================",
            "STOCK MARKET ANALYSIS REPORT",
            "==================================",
            "",
            f"Stock Symbol: {ticker_symbol}",
            f"Ticker Validation: {ticker_validation}",
            "",
            "Analysis Context:",
            f"- Data Source: yfinance daily history",
            f"- Requested History: {MIN_HISTORY_DAYS} days",
            f"- History Window: {_format_history_window(cast(pd.DataFrame, stock_data)) if isinstance(stock_data, pd.DataFrame) else 'N/A'}",
            f"- Price Change Over Window: {_format_price_change(cast(pd.DataFrame, stock_data)) if isinstance(stock_data, pd.DataFrame) else 'N/A'}",
            f"- Indicator Windows: SMA {SMA_SHORT_WINDOW}, SMA {SMA_LONG_WINDOW}, RSI {RSI_WINDOW}",
            "",
            f"Latest Close: {format_currency(indicators.get('current_price'))}",
            "",
            "Technical Indicators:",
            f"- SMA 10: {format_numeric(indicators.get('sma_10'))}",
            f"- SMA 20: {format_numeric(indicators.get('sma_20'))}",
            f"- RSI 14: {format_numeric(indicators.get('rsi_14'))}",
            "",
            f"Recommendation: {state.get('recommendation', 'HOLD')}",
            "",
            "Reason:",
            state.get("reason", "No recommendation reason available."),
            "",
            "==================================",
        ]
    )
    return {**state, "report": report}
