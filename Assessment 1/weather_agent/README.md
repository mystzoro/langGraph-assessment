# Weather Agent

A small Python project that detects user location via IP, fetches current weather from Open-Meteo, and prints a formatted weather summary.

## Environment setup (Windows)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
# or
.\.venv\Scripts\activate.bat   # cmd
```

2. Upgrade pip and install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Run the agent:

```powershell
python main.py
```

## Notes
- The project uses `requests` for HTTP calls and `pydantic` for optional schema validation.
- If `langgraph` is not available or incompatible, the project falls back to a sequential executor that preserves the original node functions and order.

## Deliverables
- [weather_agent_demo.ipynb](weather_agent_demo.ipynb) shows the fixed agent end to end with mocked API responses.
- [DEBUG_SUMMARY.md](DEBUG_SUMMARY.md) documents the bugs that were found and the fixes that were applied.
