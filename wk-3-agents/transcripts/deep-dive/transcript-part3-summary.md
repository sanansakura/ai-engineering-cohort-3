# Deep Dive Part 3 Summary

## LangChain agent with get_current_weather

- Tool implementation unchanged; pass `[get_current_weather]` as tools; create LLM (e.g. ChatOllama), then `create_agent(llm, tools)`; messages in expected dict format (role, content); `agent.invoke(messages)` runs the loop.

## Tool-calling models and registration

- **Issue**: Frameworks expect a **standard** tool-call format (JSON). Only models trained for that appear under Ollama “Tools” (e.g. Llama 3.2); **Gemma 3.1B is not** there — use **Llama 3.2** for LangChain.
- **Issue**: LangChain expects **tool objects**, not raw functions. Use **`@tool`** decorator; docstring becomes description; then pass the decorated function in the tools list.

## Single-argument constraint

- LangChain tools must take **one argument**. For `get_current_weather(city, unit)` add a wrapper: `get_weather_city(city: str) -> str` that calls `get_current_weather(city)` (unit default). Alternatively use a single dict argument for city + unit.
- After fixing model and decorator, agent works; loop runs internally.

## Transition to web search agent

- Next: replace toy weather tool with a **web search** tool; same pattern (define tool, register, create agent). DDGS (DuckDuckGo) for prototyping; for production consider Tavily or similar. Then implement `search_web` and wire it into the agent.
