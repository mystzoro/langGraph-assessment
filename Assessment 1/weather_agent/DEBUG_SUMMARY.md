Debugging Summary

Bugs found and fixes applied:

1. `main.py` entrypoint incorrect
   - Bug: Used `if __name__ == "_main_"` which never runs.
   - Fix: Change to `if __name__ == "__main__":` and use a plain `dict` for state to avoid TypedDict instantiation issues.

2. `components/config.py` had duplicate and empty variables
   - Bug: `WEATHER_API_BASE_URL` redeclared as empty string; `TEMP_MIN` was malformed.
   - Fix: Restore correct Open-Meteo URL and set `TEMP_MIN` to `"unknown"`.

3. `components/helper_functions.py` temperature classification
   - Bug: Early `if temp_celsius:` returned wrong value and blocked comparisons.
   - Fix: Treat `None` specially, otherwise perform numeric comparisons.

4. `components/nodes.py` location and weather parsing
   - Bug: Validation used `country` but API returns `country_name`; `location_data` was set to an empty dict; weather params and unit handling were inconsistent.
   - Fix: Validate `country_name`, normalize location fields, convert latitude/longitude to floats, call Open-Meteo with proper params, and format wind unit correctly.

5. `graph.py` workflow edges and LangGraph handling
   - Bug: The flow skipped the `fetch_weather_data` node and assumed LangGraph API behavior without guard.
   - Fix: Ensure linear edges include `fetch_weather_data`; attempt to use LangGraph if available, otherwise provide a sequential fallback exposing `invoke(state)`.

6. `requirements.txt` was encoded incorrectly and malformed
   - Fix: Recreated a UTF-8 `requirements.txt` with required packages.

Result: Project runs even if `langgraph` is missing; nodes operate in the intended order and produce a formatted weather summary.
