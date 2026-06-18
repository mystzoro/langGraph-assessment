"""Pytest coverage for the stock analysis agent."""

from __future__ import annotations

import pandas as pd
import pytest

from components.helper_functions import fetch_stock_history, validate_ticker_symbol
from components.indicators import calculate_indicators
from graph import build_graph


def build_mock_history_frame() -> pd.DataFrame:
    """Create deterministic stock data for testing."""

    dates = pd.date_range(end=pd.Timestamp.today(), periods=60, freq="D")
    close_prices = pd.Series(range(100, 160), dtype=float)
    return pd.DataFrame({"Close": close_prices.values}, index=dates)


class MockTicker:
    """Simple yfinance ticker mock."""

    def __init__(self, history_frame: pd.DataFrame | None = None, error: Exception | None = None):
        self.history_frame = history_frame
        self.error = error

    def history(self, *args, **kwargs):  # noqa: D401, ANN001, ANN003
        if self.error:
            raise self.error
        return self.history_frame.copy() if self.history_frame is not None else pd.DataFrame()


def test_validate_ticker_symbol_accepts_valid_symbol() -> None:
    assert validate_ticker_symbol(" aapl ") == "AAPL"


def test_validate_ticker_symbol_rejects_invalid_symbol() -> None:
    with pytest.raises(ValueError):
        validate_ticker_symbol("bad ticker!")


def test_fetch_stock_history_valid_ticker(monkeypatch: pytest.MonkeyPatch) -> None:
    import components.helper_functions as helper_functions

    monkeypatch.setattr(helper_functions.yf, "Ticker", lambda symbol: MockTicker(build_mock_history_frame()))

    history = fetch_stock_history("AAPL")
    assert not history.empty
    assert "Close" in history.columns


def test_fetch_stock_history_empty_response(monkeypatch: pytest.MonkeyPatch) -> None:
    import components.helper_functions as helper_functions

    monkeypatch.setattr(helper_functions.yf, "Ticker", lambda symbol: MockTicker(pd.DataFrame()))

    with pytest.raises(ValueError, match="No historical data returned"):
        fetch_stock_history("AAPL")


def test_fetch_stock_history_api_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    import components.helper_functions as helper_functions

    monkeypatch.setattr(
        helper_functions.yf,
        "Ticker",
        lambda symbol: MockTicker(error=ConnectionError("network failure")),
    )

    with pytest.raises(RuntimeError, match="Failed to fetch data"):
        fetch_stock_history("AAPL")


def test_indicator_calculation_correctness() -> None:
    data = build_mock_history_frame()
    indicators = calculate_indicators(data)

    assert round(indicators["current_price"], 2) == 159.00
    assert round(indicators["sma_10"], 2) == 154.50
    assert round(indicators["sma_20"], 2) == 149.50
    assert indicators["rsi_14"] == 100.0


def test_graph_happy_path(monkeypatch: pytest.MonkeyPatch) -> None:
    import components.helper_functions as helper_functions

    monkeypatch.setattr(helper_functions.yf, "Ticker", lambda symbol: MockTicker(build_mock_history_frame()))

    agent = build_graph()
    final_state = agent.invoke({"ticker_symbol": "AAPL"})

    assert final_state["recommendation"] in {"BUY", "HOLD", "SELL"}
    assert "STOCK MARKET ANALYSIS REPORT" in final_state["report"]
    assert "Ticker Validation: Passed" in final_state["report"]
    assert "Analysis Context:" in final_state["report"]
    assert "History Window:" in final_state["report"]
    assert final_state.get("error") is None


def test_graph_invalid_ticker(monkeypatch: pytest.MonkeyPatch) -> None:
    import components.helper_functions as helper_functions

    monkeypatch.setattr(helper_functions.yf, "Ticker", lambda symbol: MockTicker(build_mock_history_frame()))

    agent = build_graph()
    final_state = agent.invoke({"ticker_symbol": "INVALID TICKER"})

    assert final_state.get("error")
    assert "Ticker Validation: Failed" in final_state["report"]
    assert "Invalid ticker symbol" in final_state["report"]
