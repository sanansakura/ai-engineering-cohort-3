# Deep Dive Part 1 Summary

## Session setup and intro

- Week 4 deep dive of Project 3 (Ask the Web Agent); line-by-line walkthrough, then Q&A.
- Project 4 (deep research) already released; install via Conda or UV (UV faster); optional multi-agent part.
- Reminders: add projects to project dashboard; join Discord (alumni/knowledge sharing).

## Ask the Web Agent and tool calling

- Goal: LLM + tools + agent runtime → search the web, collect information, return results (e.g. “recent events in Boston/San Francisco”).
- Approach: start simple (basic LLM, manual tools), then iterate; key component is **tool calling**.

## Environment and models

- UV: `uv venv`, activate, `uv pip install -r requirements.txt`; isolated env; project uses latest LangChain/LangGraph (more modular).
- Ollama: run `ollama serve`; use Gemma 3 and Llama 3.2 (already pulled).

## First tool: get_current_weather (manual)

- Implement `get_current_weather(city, unit="celsius")` — dummy return (e.g. "23 {unit} and sunny in {city}"); can swap for real API later.
- **System prompt**: assistant can call tools; when user needs fresh data, respond only with a JSON-like **tool_call**; LLM must follow this format so output is parseable.
- **Tool spec** (separate string): one tool — name `get_current_weather`, description, arguments (city, unit). Appended to system content in messages.

## Calling the model (OpenAI-compatible client)

- OpenAI client with `base_url` for Ollama; model e.g. `gemma3.1b`; `messages`: system (prompt + tool_spec) + user question; `temperature=0`.
- Extract output: `response.choices[0].message.content`. Model produces structured tool call (e.g. get_current_weather for San Diego) — core of tools/agents.
