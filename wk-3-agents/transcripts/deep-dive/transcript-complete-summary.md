# Deep Dive (Project 3 — Ask the Web Agent) Complete Summary

High-level overview: Week 4 deep dive walks through Project 3 (Ask the Web Agent) line by line: foundations of tool calling with a toy weather function, parsing and agent loop, standardizing tools with types and docstrings, then LangChain agents, web search with DDGS, optional MCP and Chainlit UI, and an extended Q&A on tool standards, models, caching, and developer evolution.

---

## Session and project context

- Deep dive is for **Project 3 (Ask the Web Agent)**; next project is **Project 4 (deep research)** — already released; optional part extends to multi-agent deep research.
- Setup: **Conda or UV** (UV faster); `uv venv`, activate, `uv pip install -r requirements.txt`; project uses **latest LangChain and LangGraph** (more modular, steeper learning curve).
- Reminders: add projects to **project dashboard**; **Discord** for alumni and knowledge sharing; demo day order follows dashboard list.

## Goals and architecture

- **Ask the Web Agent**: LLM + tools + agent runtime → search the web, collect information, return results (e.g. “recent events in Boston/San Francisco”). Start simple (manual tools), then iterate; **tool calling** is the core concept that generalizes to agents.

---

## Tool calling foundations (manual)

### First tool: get_current_weather

- Implement a function (e.g. `get_current_weather(city, unit="celsius")`); for the demo use a **dummy** return (e.g. "23 {unit} and sunny in {city}"); can later swap to a real weather API.
- **System prompt**: Assistant can call tools; when the user needs fresh data, respond **only** with a JSON-like **tool_call**; the LLM must follow this **exact format** so the application can parse the output.
- **Tool spec** (separate string): Describe each tool — name (e.g. `get_current_weather`), short description, arguments (city, unit). Append to system content in the message list.
- Use an **OpenAI-compatible client** (e.g. `base_url` for Ollama); send **messages** (system with prompt + tool_spec, user question); set e.g. `temperature=0`. Extract content from `response.choices[0].message.content`. The model should emit a structured tool call (e.g. for San Diego) — this is the core of tools and agents.

### Agent loop and parsing

- Agents run in a **loop**: think → observe → decide to call tools → repeat until a final answer.
- **Parsing**: Use a regex (or similar) to find the tool_call in the LLM output; extract function name and arguments (JSON); call the actual Python function; **append the result to conversation history** and send back to the LLM so it can continue or produce the final answer.
- Manual parsing and execution is the same logic that frameworks hide under the hood.

### Standardizing tools (tool schema)

- To scale: define tools with **typed** arguments, **return type**, and **docstring**. Use **inspect** (e.g. `inspect.signature`) to auto-extract name, description, and parameters and build a **tool schema**; then you don’t hand-write tool_spec for each function.
- Re-implement the weather function with types and docstring; one utility can scan all tool functions and generate the schema for the system prompt.

### Single vs multiple tool calls

- Query like “Is Boston warmer today or Seattle?” needs **two** tool calls. Smaller models (e.g. Gemma 3.1B) may emit a different format or only one call.
- **Llama 3.2 3B** can emit **two** tool calls in one response; the runtime can **parse and run them in parallel** for speed; many labs train models to produce multiple tool calls when needed.

---

## LangChain agent

### create_agent and tool-calling models

- **create_agent** (current API; no longer create_react_agent): inputs are **model** (required), **tools** (list), **system_prompt** (optional). Agent = LLM in a loop with tools.
- Frameworks expect a **standard** tool-call format (JSON). In Ollama, only models listed under **Tools** support this (e.g. **Llama 3.2**); **Gemma 3.1B** is not in that list — use a tool-calling model for LangChain.
- LangChain expects **tool objects**, not raw functions: use the **`@tool`** decorator; the **docstring** becomes the tool description. Pass the decorated function(s) in the tools list.

### Single-argument constraint

- LangChain tools must take **one argument**. For `get_current_weather(city, unit)` use a wrapper, e.g. `get_weather_city(city: str) -> str` that calls `get_current_weather(city)` with a default unit, or use a single **dict** argument (city + unit). Newer versions may relax this; share workarounds on the course portal if you find them.

### Using the agent

- Build **messages** in the format the framework expects (e.g. list of dicts with role and content). Call **agent.invoke(messages)**; the loop (call LLM → parse tool calls → run tools → append results → repeat) runs internally until the model returns a final answer.

---

## Web search agent

### search_web tool (DDGS)

- Implement e.g. `search_web(query: str, max_results: int = 10) -> str`: use **DDGS** (DuckDuckGo) `.text(query, max_results=...)`; collect results; format each as title + link; return a single string (e.g. newline-joined). **DDGS is for prototyping**; for production use search-oriented APIs (e.g. **Tavily**).
- Add docstring and **@tool**; respect single-argument (e.g. only `query`, or one dict). Reference the tool by its **registered name** (e.g. `search_web`) when creating the agent to avoid “not defined” errors.

### Web agent and run_agent_with_reasoning

- Create LLM (e.g. Llama 3.2 3B), tools `[search_web]`, then **web_agent = create_agent(llm, tools)**. **agent.invoke()** expects the framework’s message structure, not a plain string.
- Helper **run_agent_with_reasoning(agent, question)**: builds messages, runs the agent loop, **prints** tool calls and arguments for debugging, and returns the **final answer** when the model stops emitting tool calls. User normally sees only the final answer; internals are visible if you print inside the helper.

### Multi-round and improvements

- Example: “What sport events in San Francisco and Boston?” — model can emit two **search_web** calls; runtime runs them (in parallel when supported), appends results; model then produces a **final answer** and the loop stops.
- Improvements: fetch and use **page content** from URLs; switch to **Tavily** or similar for production; consider **multi-agent** setups (e.g. Perplexity-style). Optional section covers **MCP** to use external tools without implementing them yourself.

---

## Optional: MCP (Model Context Protocol)

- **Libraries**: **mcp** (core protocol) and **langchain-mcp-adapters** (bridge to LangChain). Protocol standardizes tool descriptions and invocation; adapter exposes MCP tools as LangChain tools.
- **Usage**: Create MCP client/session; use adapter to **load MCP tools** (e.g. from a server); pass the resulting tool list to **create_agent(llm, tools)**. Example: **fetch MCP server** — one tool, `fetch` (URL + optional markup). User can ask “fetch this URL and summarize the page” without writing a custom tool.
- **Filesystem MCP server**: many tools (read text file, read media, etc.). Use **session.list_tools()** to see what’s available. Can use external or self-hosted MCP servers; async/session boilerplate is typical — follow MCP and adapter docs. Instructor may add an MCP walkthrough notebook later.

---

## Optional: Chainlit UI

- **Chainlit** is built for LLM/agent UIs: define search tool, create agent, then add Chainlit UI code so that on user message the agent runs and the response is shown. Write the app to a file (e.g. `chainlit_app.py`), run **chainlit run chainlit_app.py** for a local server — result is a simple Perplexity-like chat interface.

---

## Q&A: Tool standards and interchangeability

- **Swapping tools** (e.g. different weather providers): ensure **types** and **docstring**; frameworks inject these into the system prompt. For **MCP**, the protocol **requires** description and argument types; missing them causes failures.
- **Implementing MCP servers**: follow protocol (docstring, types) and make functions **reliable** (try/except, logging, fallbacks, avoid hanging). Prefer **consuming** existing MCP services first; a few lines can expose many external tools to a LangChain agent.

---

## Q&A: Frameworks and orchestration

- **LangGraph vs LangChain**: LangGraph gives more **customization** and control; LangChain is more abstract with good defaults. Use LangGraph when you need finer control over agent flow.

---

## Q&A: Models and APIs

- **Proprietary models (OpenAI, Anthropic, etc.)**: Replace Ollama client/config with their API; check docs for keys (often paid; possible free tier). Local setup gives more control; mixing APIs and frameworks requires compatibility checks.
- **Speed**: For prototyping, local models are fine; for **production**, small local models (e.g. 3B) are often insufficient — use commercial APIs (Gemini, ChatGPT) or larger open-source models. Start simple and fast, then swap in better models.
- **Model preferences**: Instructor uses ChatGPT, Gemini (precise, less verbose), Claude (writing/editing); for coding, Claude Code then Cursor if needed. Opus 4.6 and new OpenAI products are strong; landscape changes often. **Perplexity**: early and search-focused; differentiation may decrease as others improve.

---

## Q&A: Course logistics

- **Solution and recording**: Course portal → Deep Dive Project 3 → **Files** → download solution; recording uploaded after Zoom (often within several hours). Request to compare attendee implementation (e.g. with Cursor) to instructor’s for revision.
- **Where solutions are**: Course portal → Deep Dive Project (e.g. Project 3) → Files icon → solution file.
- **Grading**: No grading or pull requests; templates are for practice and deep-dive prep; solution is released after the following Saturday deep dive.
- **Past cohorts**: Planning to allow **past cohorts** to **join demo day** (e.g. Feb 22) as viewers; presentations from current cohort only; announcement to follow. Encourage sharing answers and resources in the community.

---

## Q&A: Web search and tool guidance

- **Guidance** (which sites, how to search): Put constraints in the **system prompt**; LLMs follow such instructions well.
- **Production search**: Use APIs like **Tavily** (not DDGS): API key, methods such as `extract` for content; SDK supports filters (sites, page rank, etc.) — see their reference.

---

## Q&A: Many tools and overlapping tools

- **Multiple tools with overlapping function**: With few tools (e.g. 5–10), a capable LLM can choose; **thinking models** reason before answering. With **many tools** (100s–1000s): don’t put all in the system prompt; use **retrieval**: store tools and metadata, on each user query **retrieve top-k relevant tools** and pass only those to the agent for that turn.
- **Plan mode** (e.g. Cursor): show user planned tools and ask confirmation before executing; ecosystem is evolving (e.g. agent skills, script-based tools).

---

## Q&A: Agent behavior and debugging

- **Agent not using tool / wrong answer**: Expected flow: request → agent sees registered tool → emits tool call → runtime parses, calls function, appends result → LLM gets result and produces final answer. If the agent returns something that doesn’t match your tool (e.g. wrong unit), ensure the **registered** function is the one called and unit/defaults are correct; use a single-arg wrapper or dict; share code for debugging.
- **Tracing tool output**: Agent messages have a known structure; if a message has **tool_calls**, extract and print them in the loop (see solution’s **run_agent_with_reasoning**) to see what was called and what was returned. Frameworks typically don’t cache tool results by default; if behavior suggests caching, trace to confirm the tool is invoked each time.

---

## Q&A: Streamlit, MCP, and streaming

- **Streamlit + MCP**: Same pattern as notebook: create MCP client, load tools via adapter, pass those tools to **create_agent** instead of a custom web search tool.
- **agent.stream vs agent.invoke**: **Stream** streams tokens as the model generates; **invoke** returns after the full response. Use stream for incremental UI.

---

## Q&A: Tool execution order

- **Order of multiple tool calls**: Depends on **agent runtime**. Common behavior: when the LLM emits **multiple** tool calls, the runtime runs them **in parallel**; naive implementations may run sequentially (order may be emission order or arbitrary). For “Boston and San Francisco,” two parallel calls is typical.

---

## Q&A: Caching in inference (KV / prompt caching)

- **What is cached**: Not “cache final answers” — it’s **KV cache** on a **prefix of the prompt**. System prompt + tool spec are fixed and long; their tokenization and transformer computation can be **cached**. Next request with the same prefix (e.g. only user question or conversation tail changes) reuses cached activations — large **latency and cost** savings (e.g. up to ~80% latency, ~90% input cost in extreme cases).
- **Conversation history**: Per user; follow-up turns have growing context; that prefix is cached so later turns are faster. **Summarization**: When context nears the context-window limit, systems often summarize older conversation; until then (e.g. tens of thousands of tokens), full history is used and caching still helps. The **prompt is still full**; caching is internal (activations), not replacing prompt text. Main benefit in agents comes from **conversation history** and fixed system/tool prefix.

---

## Q&A: Developer evolution and AI coding

- **Software development evolution**: Moving very fast; hard to predict 2–3 years out. Point (e.g. Andrej Karpathy): much coding is “writing messages to Claude Code,” which can feel uncomfortable for strong engineers. Advice: **stay current** with tools (Cursor, Claude Code, etc.) and learn **effective prompting and interaction**; these are valuable for now but keep evolving.

---

## Key takeaways

- **Tool calling**: LLM + tool spec (name, description, args) in system prompt → model emits structured tool_call → parse, execute function, append result to history → repeat until final answer. This is the core of agents; frameworks automate the loop and parsing.
- **Standards**: Typed arguments, return type, and docstring enable auto tool schema; MCP requires them. Use tool-calling models (e.g. Llama 3.2) with LangChain; single-argument wrapper if needed.
- **Web agent**: Same pattern with `search_web` (DDGS for prototyping, Tavily for production); helper like run_agent_with_reasoning for debugging and correct invoke format.
- **MCP**: Use existing MCP servers and adapters to get many tools without implementing each one; Chainlit for a simple chat UI.
- **At scale**: Use retrieval to select relevant tools per query instead of putting hundreds of tools in the prompt; plan mode and tool confirmation are emerging patterns.
- **Caching**: KV/prompt caching on prefix (system + tools + conversation) reduces cost and latency; summarization kicks in when context is large.
