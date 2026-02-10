# Deep Dive Part 2 Summary

## Agent loop and parsing tool calls

- Agents run in a **loop**: think → observe → decide to call tools → repeat until final answer.
- Need to **parse** LLM output (regex), extract function name and arguments (JSON), call the real function, then append results to conversation and send back to LLM.

## Parsing and executing

- Pattern match on tool_call in output; from match, load JSON, get `name` and `arguments`; call `get_current_weather(**arguments)`; result (e.g. "23 C") must be appended to history and sent back — that’s the agent loop.
- Manual process gets unwieldy with more tools; next step: **standardize** tool definitions.

## Standardizing tools (tool schema)

- Tools: **typed** arguments, **return type**, and **docstring**. Use `inspect.signature` (and similar) to auto-extract name, description, parameters and build a tool schema.
- Re-implement `get_current_weather` with types and docstring; single function can scan all tools and generate schema; no more hand-written tool_spec.

## Single vs multiple tool calls

- Query “Is Boston warmer today or Seattle?” → need **two** tool calls. Gemma 3.1B sometimes produced wrong format or only one call.
- **Llama 3.2 3B**: produces **two** tool calls in one response; parse both and run in **parallel** for speed; many labs train models to emit multiple tool calls when needed.

## Switching to LangChain

- LangChain implements the same loop and tool handling; `create_agent` (new API; no more create_react_agent). Inputs: **model** (required), **tools** (list), **system_prompt** (optional). Agent = LLM in a loop with tools.
