"""LangGraph workflow for stock analysis."""

from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from components.nodes import (
    calculate_indicators_node,
    fetch_stock_data_node,
    format_analysis_report_node,
    generate_recommendation_node,
)


class StockAnalysisState(TypedDict, total=False):
    """Shared state passed between LangGraph nodes."""

    ticker_symbol: str
    ticker_validation: str
    stock_data: object
    indicators: dict[str, float]
    recommendation: str
    reason: str
    report: str
    error: str


def build_graph():
    """Construct and compile the stock analysis graph."""

    workflow = StateGraph(StockAnalysisState)
    workflow.add_node("fetch_stock_data", fetch_stock_data_node)
    workflow.add_node("calculate_indicators", calculate_indicators_node)
    workflow.add_node("generate_recommendation", generate_recommendation_node)
    workflow.add_node("format_analysis_report", format_analysis_report_node)

    workflow.add_edge(START, "fetch_stock_data")
    workflow.add_edge("fetch_stock_data", "calculate_indicators")
    workflow.add_edge("calculate_indicators", "generate_recommendation")
    workflow.add_edge("generate_recommendation", "format_analysis_report")
    workflow.add_edge("format_analysis_report", END)

    return workflow.compile()
