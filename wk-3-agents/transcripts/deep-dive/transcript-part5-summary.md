# Deep Dive Part 5 Summary

## LangChain tool single-argument workaround

- Wrapper `get_weather_city(city: str)` calls `get_current_weather(city)`; register the wrapper with `@tool`; docstring required. Newer LangChain may support multi-arg tools; share workarounds on course portal if found.

## Web search implementation (DDGS)

- `search_web(query, max_results=10)`: DDGS object, `ddgs.text(query, max_results=...)`, format each result (title, link), return `"\n".join(...)`. Test with a query; register with `@tool`, create web agent (Llama 3.2, `[search_web]`). Fix: use `search_web` in tools list (name mismatch causes “not defined” if wrong).

## Optional: MCP (Model Context Protocol)

- Two libraries: **mcp** (core protocol) and **langchain-mcp-adapters** (bridge to LangChain). Same idea as before: protocol defines how tools are described and invoked; adapter exposes MCP tools as LangChain tools.
- Example: **fetch MCP server** — one tool, `fetch` (fetch URL, optional markup). Create MCP client/session, load tools via adapter (`load_mcp_tools` or similar), get list of tools; pass to `create_agent(llm, tools)`. User message e.g. “fetch this URL and summarize the page”; no custom tool implementation — tools come from MCP server.
- Async/session boilerplate is typical; follow MCP and adapter docs. Another example: **filesystem MCP server** with many tools (read text file, read media, etc.). Can use external or self-hosted MCP servers; instructor may add an MCP walkthrough notebook later.
