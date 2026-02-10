# Deep Dive Part 6 Summary

## MCP wrap-up

- Fetch server: single `fetch` tool. File system server: many tools (read text file, read media, etc.). Use `session.list_tools()` to see available tools; incorporate external or local MCP servers into LangChain agents via adapters.

## Optional: Chainlit UI

- UI frameworks: Streamlit, others; **Chainlit** is aimed at LLM/agent UIs — docs, components, write Python and get a chat UI.
- Assemble: define search tool, create agent (Llama 3.2, search_web), then Chainlit UI code — on user message, run agent and display response. Write full app to e.g. `chainlit_app.py` (or from notebook with a write-file cell), then run `chainlit run chainlit_app.py` for local server.
- Result: simple Perplexity-like interface — user types query, agent uses web search and returns answer. Session wrap-up; move to Q&A.

## Q&A (start)

- Upload: solution code on course portal (deep dive project three, Files); recording uploaded after Zoom processing (often within several hours).
- Request: compare attendee’s implementation (e.g. with Cursor) to instructor’s for revision.
