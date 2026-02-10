# Deep Dive Part 8 Summary

## Q&A: Solution location and grading

- **Where**: Course portal → Deep Dive Project 3 → Files icon → download solution and open in IDE.
- **Grading**: No grading or pull requests; templates are for practice and deep-dive prep; following Saturday deep dive implements and releases solution.

## Q&A: Web search guidance and production

- **Guidance** (which sites, how to search): put constraints in **system prompt**; LLMs follow such instructions well.
- **Production search**: DDGS is for prototyping; for real apps use search-oriented APIs (e.g. **Tavily**): API key, methods like `extract` for content; SDK supports filters (sites, page rank, etc.) — check their reference.

## Q&A: Overlapping tools and tool selection

- **Multiple tools with overlapping function**: For few tools (e.g. 5–10), a good LLM can choose; **thinking models** reason before answering. For **many tools** (100s–1000s): don’t put all in system prompt; use a **retrieval** step: store tools + metadata, on each user query retrieve top-k relevant tools and give only those to the agent for that turn.
- **Plan mode** (e.g. Cursor): one pattern — show user planned tools and ask confirmation before executing; ecosystem is evolving (e.g. agent skills, script-based tools).

## Q&A: Agent not calling tool / workflow

- Expected flow: request → agent sees registered tool → emits tool call (e.g. get_weather, city San Diego) → runtime parses, calls function, gets result → result appended to history and sent back to LLM → LLM produces final answer. If agent returns something else (e.g. 25°F instead of hardcoded 23°C), check that the **registered** function is the one actually called and that unit handling (default Celsius) is correct. Can use wrapper with single arg (city) or dict (city + unit); share code for debugging if needed.

## Q&A: Streamlit + MCP; stream vs invoke

- **Streamlit + MCP**: Same as notebook: create MCP client, load tools via adapter, pass those tools to `create_agent` instead of custom web search; rest unchanged.
- **agent.stream vs agent.invoke**: **Stream** allows streaming tokens as the model generates; **invoke** waits for full response then returns; use stream for nicer incremental UI.

## Q&A: Order of multiple tool calls

- **Who decides order**: Depends on **agent runtime** implementation. Typical: if LLM emits **multiple** tool calls, runtime runs them **in parallel** (efficient); naive implementations may run sequentially (order might be emission order or arbitrary). For “Boston and San Francisco,” two calls in parallel is expected.

## Q&A: Tracing tool output and caching

- **Tracing**: Agent messages have a known structure; if `message` has `tool_calls`, that’s a tool-calling request; extract and print in a loop (see solution’s run_agent_with_reasoning) to inspect what was called and what was returned.
- **Caching (weather not updating)**: Frameworks typically don’t cache tool results by default; if behavior suggests otherwise, trace tool calls to confirm the tool is actually invoked each time.

## Q&A: KV / prompt caching (inference)

- **Caching in inference** (e.g. Ollama, vLLM): Not “cache query answers” — it’s **KV cache** on a **prefix of the prompt**. System prompt + tool spec are fixed and long; they’re tokenized and run through transformer; that computation is cached. Next request with same prefix (e.g. only user question changes) reuses cached activations for that prefix — big **latency and cost** savings (e.g. 80% latency, 90% input cost in extreme cases).
- **Conversation history**: Per-user; follow-up turns have growing context; that prefix is also cached so later turns are faster. **Summarization**: When context nears context-window limit, systems often summarize older conversation; until then (e.g. 30k+ tokens), full history is used and caching helps. Prompt stays full; caching is internal (activations), not swapping text.

## Q&A: Developer evolution and AI coding

- **Software development evolution**: Moving very fast; hard to predict 2–3 years out. Andrej Karpathy’s point: much coding is “writing messages to Claude Code,” which can feel uncomfortable for strong engineers. Advice: stay current with tools (e.g. Cursor, Claude Code), learn effective prompting and interaction; these are valuable for now but keep changing.

## Session end

- Recordings of previous deep dives on course portal. Enjoy weekend; see you next Wednesday; new content on thinking and reasoning models.
