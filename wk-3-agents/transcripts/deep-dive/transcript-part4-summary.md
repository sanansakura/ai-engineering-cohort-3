# Deep Dive Part 4 Summary

## Web search tool (DDGS)

- `search_web(query: str, max_results: int = 10) -> str`: use DDGS `.text()`; collect results; format as title + link per line; return joined string. For production, use APIs like Tavily; can also fetch page bodies from URLs.

## Registering and creating web agent

- Add docstring and `@tool`; single-argument (query only; max_results fixed or via dict). Create LLM (Llama 3.2 3B), tools `[search_web]`, then `web_agent = create_agent(llm, tools)`. Use `search_web` (not “web search”) in code when referencing the tool.

## Invoke and run_agent_with_reasoning

- `agent.invoke()` doesn’t accept a plain string; use the expected message format. Helper **run_agent_with_reasoning(agent, question)** builds messages, runs loop, prints tool calls and args for debugging, and returns final answer when the model stops emitting tool calls.

## Multi-round and final answer

- Example: “What sport events in San Francisco and Boston?” — model emits two search_web calls (SF, Boston); runtime parses, runs (can be parallel), appends results; model then produces **final answer** (no tool call), loop stops. Final answer is what the user sees; internals visible only if you print inside the helper.

## Improvements and optional MCP

- Improvements: extract page content from URLs; switch to better search APIs; consider multi-agent (e.g. Perplexity-style). Optional section: **MCP** (Model Context Protocol) — use existing MCP servers/tools instead of implementing everything yourself.
