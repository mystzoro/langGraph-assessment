"""
Graph definition for the Weather Agent.

We attempt to use LangGraph's StateGraph if available. If LangGraph is not present
or its API is incompatible, fall back to a simple sequential executor that exposes
an `invoke(state)` method so `main.py` can run the workflow.
"""

from components.state import WeatherAgentState
from components.nodes import (
    fetch_location_data,
    fetch_weather_data,
    generate_weather_info,
)

try:
    from langgraph.graph import StateGraph, START, END
    # Build the StateGraph in proper order
    builder = StateGraph(WeatherAgentState)
    builder.add_node("fetch_location_data", fetch_location_data)
    builder.add_node("fetch_weather_data", fetch_weather_data)
    builder.add_node("generate_weather_info", generate_weather_info)

    # Linear flow: start -> fetch_location -> fetch_weather -> generate_info -> end
    builder.add_edge(START, "fetch_location_data")
    builder.add_edge("fetch_location_data", "fetch_weather_data")
    builder.add_edge("fetch_weather_data", "generate_weather_info")
    builder.add_edge("generate_weather_info", END)

    # Expose the builder which should have an `invoke`-like API
    # Some versions of langgraph's StateGraph do not provide an `invoke` method;
    # in that case, provide a small adapter that runs the nodes in the intended order.
    if hasattr(builder, "invoke"):
        weather_agent = builder
    else:
        class LangGraphAdapter:
            def __init__(self, nodes):
                self.nodes = nodes

            def invoke(self, state):
                if not isinstance(state, dict):
                    try:
                        state = dict(state)
                    except Exception:
                        raise TypeError("State must be a dict-like object")
                for fn in self.nodes:
                    state = fn(state)
                return state

        weather_agent = LangGraphAdapter([
            fetch_location_data,
            fetch_weather_data,
            generate_weather_info,
        ])
except Exception:
    # Fallback sequential executor
    class SequentialAgent:
        def __init__(self, nodes):
            self.nodes = nodes

        def invoke(self, state):
            # Ensure state is a mutable dict-like object
            if not isinstance(state, dict):
                try:
                    state = dict(state)
                except Exception:
                    raise TypeError("State must be a dict-like object")

            for fn in self.nodes:
                state = fn(state)
            return state

    weather_agent = SequentialAgent([
        fetch_location_data,
        fetch_weather_data,
        generate_weather_info,
    ])