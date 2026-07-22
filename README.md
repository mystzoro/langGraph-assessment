<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=LangGraph%20Assessment&fontSize=50&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Weather%20Agent%20%7C%20Stock%20Market%20Analysis%20Agent&descAlignY=58&descAlign=62" />

  <br />

  [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
</div>

---

## 🧠 About

This repository contains two Python assignments demonstrating **debugging, workflow development, state management, API integration, testing, and AI agent development with LangGraph**.

---

## 📋 Assignment 1 — Weather Agent Debugging

### Objective
Debug and fix a broken LangGraph-based weather agent.

### Features
- 🌍 IP-based location detection
- 🌤️ Weather data retrieval via API integration
- 🔁 LangGraph workflow execution
- ⚠️ Error handling and input validation
- 🧪 Unit testing with Pytest
- 📝 Documentation of all fixes applied

### Workflow

```
START
  ↓
fetch_location_data   (IP → City/Country)
  ↓
fetch_weather_data    (City → Weather API)
  ↓
generate_weather_info (Format output)
  ↓
END
```

### Bugs Fixed

| Bug | Fix Applied |
|---|---|
| Missing API error handling | Added try/except with meaningful error messages |
| Wrong state key access | Fixed key names to match LangGraph state schema |
| No input validation | Added checks for empty/null location data |
| Broken workflow transitions | Corrected edge definitions in graph builder |

### Tech Stack
- Python 3.10+
- LangGraph
- Requests
- Pytest

---

## 📈 Assignment 2 — Stock Market Analysis Agent

### Objective
Build a stock market analysis agent using LangGraph that provides actionable trading recommendations.

### Features
- 📅 Fetches **60 days** of historical stock data
- 📊 Calculates **SMA (10-day)** — Short-term moving average
- 📊 Calculates **SMA (20-day)** — Long-term moving average
- 📉 Calculates **RSI (14-day)** — Relative Strength Index
- 🤖 Generates **BUY / HOLD / SELL** recommendation
- ⚠️ Error handling for invalid symbols or API failures
- 🧪 Automated tests with Pytest

### Recommendation Logic

| Condition | Signal |
|---|---|
| SMA10 > SMA20 AND RSI < 70 | **BUY** |
| RSI > 70 | **SELL** (overbought) |
| RSI < 30 | **BUY** (oversold) |
| Otherwise | **HOLD** |

### Workflow

```
START
  ↓
fetch_stock_data       (60-day historical OHLCV)
  ↓
calculate_indicators   (SMA10, SMA20, RSI14)
  ↓
generate_recommendation (BUY/HOLD/SELL)
  ↓
END
```

### Tech Stack
- Python 3.10+
- LangGraph
- yfinance (stock data)
- pandas / numpy (calculations)
- Pytest

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+

### Installation

```bash
# Clone the repo
git clone https://github.com/mystzoro/langGraph-assessment.git
cd langGraph-assessment

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Assignment 1 (Weather Agent)

```bash
cd assignment1
python main.py
```

### Run Assignment 2 (Stock Agent)

```bash
cd assignment2
python main.py --symbol AAPL
```

### Run Tests

```bash
# All tests
pytest

# Assignment-specific
pytest assignment1/tests/
pytest assignment2/tests/
```

---

## 📁 Project Structure

```
langGraph-assessment/
├── assignment1/
│   ├── weather_agent.py    # Fixed LangGraph weather agent
│   ├── main.py             # Entry point
│   ├── tests/              # Pytest test suite
│   └── FIXES.md            # Documentation of bugs and fixes
├── assignment2/
│   ├── stock_agent.py      # Stock analysis LangGraph agent
│   ├── indicators.py       # SMA & RSI calculations
│   ├── main.py             # Entry point
│   └── tests/              # Pytest test suite
├── requirements.txt
└── README.md
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  Made with ❤️ by <a href="https://priyanshuchand.netlify.app/">Priyanshu Chand</a>
</div>
