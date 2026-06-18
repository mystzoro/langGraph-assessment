# Debug Summary

## Implementation Notes

- Built the agent as a LangGraph pipeline with four explicit stages: fetch, calculate, recommend, and format.
- Kept shared state narrow and typed so each node only mutates the fields it owns.
- Centralized ticker validation in a helper and surfaced its result in the final report so the analysis includes explicit input-quality context.
- Expanded the report to include history range, window change, and indicator settings instead of only a minimal formatted snapshot.

## Error Handling

- Invalid ticker symbols are rejected before analysis begins.
- Empty responses from `yfinance` are converted into a structured error.
- Calculation failures and missing data are surfaced as readable report messages instead of raw exceptions.
- The CLI exits with a non-zero status when the workflow produces an error.

## Testing Approach

- Added pytest coverage for valid data, invalid tickers, empty responses, API failures, and indicator correctness.
- Mocked `yfinance` so the tests stay deterministic and do not depend on network access.

## Quality Choices

- Used descriptive names, type hints, and docstrings throughout.
- Kept the recommendation engine rule-based and transparent so it is easy to explain in an assessment.
- Structured the project for GitHub readiness with a local virtual environment and clean ignore rules.
