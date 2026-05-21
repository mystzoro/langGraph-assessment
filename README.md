# LangGraph Assessment

This repository contains two Python assignments that demonstrate debugging, workflow development, state management, API integration, testing, and AI agent development with LangGraph.

---

## Assignment 1 - Weather Agent Debugging

### Objective
Debug and fix a broken LangGraph-based weather agent.

### Features
- IP-based location detection
- Weather retrieval using API integration
- LangGraph workflow execution
- Error handling and validation
- Unit testing
- Documentation of fixes

### Workflow

START -> fetch_location_data -> fetch_weather_data -> generate_weather_info -> END

### Technologies
- Python
- LangGraph
- Requests
- Pytest

---

## Assignment 2 - Stock Market Analysis Agent

### Objective
Build a stock market analysis agent using LangGraph.

### Features
- Fetches 60 days of historical stock data
- Calculates SMA (10 Day)
- Calculates SMA (20 Day)
- Calculates RSI (14 Day)
- Generates BUY, HOLD, or SELL recommendation
- Error handling
- Automated tests
- Jupyter Notebook demonstration

### Workflow

START -> fetch_stock_data -> calculate_indicators -> generate_recommendation -> format_analysis_report -> END

### Technologies
- Python
- LangGraph
- Pandas
- NumPy
- yfinance
- Pytest
- Jupyter Notebook

---

## Repository Structure

```text
langGraph-assessment/
|
|-- Assessment 1/
|   \-- weather_agent/
|
\-- Assessment 2/
    |-- components/
    |-- tests/
    |-- graph.py
    |-- main.py
    |-- README.md
    |-- requirements.txt
    \-- stock_agent_demo.ipynb
```

## Setup

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r "Assessment 1/weather_agent/requirements.txt"
pip install -r "Assessment 2/requirements.txt"
```

---

## Author

Priyanshu Chand