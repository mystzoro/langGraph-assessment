"""Command-line entry point for the stock market analysis agent."""

from __future__ import annotations

import argparse
import sys

from components.helper_functions import print_report
from graph import build_graph


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Run the LangGraph stock market analysis agent."
    )
    parser.add_argument(
        "ticker",
        nargs="?",
        help="Stock ticker symbol such as AAPL, MSFT, or TSLA.",
    )
    return parser.parse_args()


def main() -> int:
    """Run the agent and print the formatted report."""

    args = parse_arguments()
    ticker_symbol = (args.ticker or input("Enter a stock ticker symbol: ")).strip().upper()

    agent = build_graph()
    final_state = agent.invoke({"ticker_symbol": ticker_symbol})

    report = final_state.get("report")
    if report:
        print_report(report)

    if final_state.get("error"):
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
