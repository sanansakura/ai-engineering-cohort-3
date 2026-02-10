# Office Hours Transcript Part 4 Summary

## Codex and MCP Servers
- Codex app: add MCP servers (local, HTTP, stdio)
- Once added, Codex knows and can use those tools

## General Purpose vs. Domain-Specific LLMs
- Chatbots (ChatGPT, Gemini, etc.): **general-purpose** LLMs
- ChatGPT: e.g., GPT 5.2 instant (non-thinking) and GPT 5.2 thinking
- Same models accessible via API (commercial, may require payment)

## Memory: Short-Term vs. Long-Term

### Short-Term Memory
- Equals **context window**
- Whatever is in context is what the LLM sees at each step

### Long-Term Memory
- Stored **outside** context
- Loaded on demand based on current input
- Examples: user preferences, retrieval from knowledge base (RAG)

### Flow
- Long-term data (e.g., RAG chunks) is retrieved and **moved into** short-term memory (context)

### Coding Agents
- Entire codebase in long-term storage (embedded, RAG-style)
- Retrieval fetches relevant chunks into active context
- Entire codebase does not fit in context
