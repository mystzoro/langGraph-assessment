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
from components.indicators import calculate_indicators


def fetch_stock_data_node(state: dict) -> dict:
    """Fetch and validate stock data."""

    if state.get("error"):
        return state

    ticker_symbol = state.get("ticker_symbol", "")
    try:
        normalized_symbol = validate_ticker_symbol(ticker_symbol)
        stock_data = fetch_stock_history(normalized_symbol)
        return {**state, "ticker_symbol": normalized_symbol, "stock_data": stock_data}
    except Exception as exc:  # noqa: BLE001 - converted to workflow state
        return {**state, "error": str(exc)}


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
    indicators = cast(dict[str, float], state.get("indicators") or {})

    if state.get("error"):
        report = "\n".join(
            [
                "==================================",
                "STOCK MARKET ANALYSIS REPORT",
                "==================================",
                "",
                f"Stock Symbol: {ticker_symbol}",
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
            f"Current Price: {format_currency(indicators.get('current_price'))}",
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
