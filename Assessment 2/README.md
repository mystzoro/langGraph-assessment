# Stock Market Analysis Agent

This project is a LangGraph-based stock analysis tool that fetches recent market data for a ticker, calculates technical indicators, and generates a readable BUY, HOLD, or SELL recommendation.

## Project Description

The agent accepts a stock ticker symbol, downloads the latest 60 days of price history with `yfinance`, calculates SMA 10, SMA 20, and RSI 14, then formats the result into a clean report.

## Features

- Accepts a ticker such as `AAPL`, `MSFT`, or `TSLA`
- Fetches the last 60 days of historical data
- Calculates SMA 10, SMA 20, and RSI 14
- Generates a rule-based recommendation
- Handles invalid tickers, empty responses, and API failures
- Uses a simple LangGraph workflow with shared state

## Installation

Create and activate a virtual environment from the project root:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py AAPL
```

If no ticker is provided, the program prompts for one interactively.

## Example Output

```text
==================================
STOCK MARKET ANALYSIS REPORT
==================================

Stock Symbol: AAPL
Current Price: $159.00

Technical Indicators:
- SMA 10: 154.50
- SMA 20: 149.50
- RSI 14: 100.00

Recommendation: HOLD

Reason:
Momentum and RSI signals do not provide a clear directional edge.

==================================
```

## Workflow

The graph runs in this order:

1. Fetch stock data
2. Calculate indicators
3. Generate recommendation
4. Format the final report

Each node reads and returns the same shared state, which keeps the flow easy to trace and maintain.

## Notebook

Open `stock_agent_demo.ipynb` for a polished walkthrough with these sections:

1. Project Overview
2. Architecture
3. Implementation
4. Test Cases
5. Results
6. Conclusion

## Testing

Run the automated checks with:

```bash
pytest
```

The tests mock `yfinance` so they stay deterministic and do not require network access.

## Repository Structure

- `components/`: helper functions, indicators, and LangGraph nodes
- `tests/`: pytest coverage for the workflow and utility functions
- `graph.py`: shared state and graph assembly
- `main.py`: command-line entry point
- `README.md`: project overview and usage
- `DEBUG_SUMMARY.md`: implementation notes and testing summary
- `requirements.txt`: required packages
- `stock_agent_demo.ipynb`: submission notebook

## GitHub Readiness

The repository is configured to ignore the local virtual environment, Python caches, notebook checkpoints, and test artifacts.
