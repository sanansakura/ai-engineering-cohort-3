# Deep Dive Part 7 Summary

## Q&A: Tool standards and interchangeability

- Swapping tools (e.g. GetWeather vs GetWeather2): ensure **types** and **docstring**; frameworks use these for system prompt. For **MCP**, protocol requires description and argument types — mandatory for MCP servers; otherwise tooling fails.
- Own MCP servers: follow protocol (docstring, types) and make functions **reliable** (try/except, logging, fallbacks, don’t hang). Prefer **consuming** existing MCP services first; with a few lines you can use many external tools via session + list_tools + pass to LangChain agent.

## Q&A: LangGraph vs LangChain

- LangGraph offers more **customization** and control than LangChain; LangChain is more abstract with good defaults. Use LangGraph when you need finer control over agent behavior.

## Q&A: Proprietary models and speed

- **OpenAI/Anthropic etc.**: replace Ollama client/config with their API (same idea); check docs for API keys (often paid; possible free tier). Local = more control; different APIs/frameworks require compatibility checks.
- **Speed**: prototyping locally is fine; for production, small local models (e.g. 3B) often insufficient — use commercial APIs (Gemini, ChatGPT) or large open-source. Start simple and fast, then swap in better models.

## Q&A: Model preferences and Perplexity

- Instructor: started with ChatGPT, then Gemini (often more precise, less verbose), then Claude (e.g. writing, editing); for coding: Claude Code then Cursor if needed. Opus 4.6 and new OpenAI products are strong; landscape changes often; Perplexity was early and search-focused but may be less differentiated as others improve.

## Q&A: Past cohorts and demo day

- Planning to let **past cohorts** join **demo day** (Feb 22) as viewers; presentations from current cohort only; same for future cohorts. Announcement to follow. Questions/discussion still welcome after course; encourage sharing answers and resources.
