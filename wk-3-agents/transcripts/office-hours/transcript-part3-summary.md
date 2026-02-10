# Office Hours Transcript Part 3 Summary

## Hugging Face and Model Discovery
- **Hugging Face Hub** (huggingface.co): browse models, trending, filters
- Example: search “Qwen K2”; use model page → “Use this model” → copy code for Transformers
- Documented usage for vLLM and other backends

## Input Format: JSON vs. Markdown
- Depends on how the model was trained
- **Markdown** preferred for most LLMs (system prompts often in markdown)
- **JSON** when it fits (API payloads, coding artifacts)
- Don’t convert JSON to markdown when it doesn’t make sense (e.g., DB query results)

## Skills (Markdown-on-File / Skill.md)

### Structure
- Skill = folder with `skill.md` (required), optional scripts, optional resources
- Metadata: `name`, `description` (required) at top of SKILL.md
- Used to build metadata sent to LLM at start

### Loading Flow
- Agent runtime builds metadata (skill names + descriptions) → includes in context
- LLM sees available skills; when needed, issues **open_file** tool call with skill path
- Agent loads `skill.md`, appends to context, LLM continues
- Scripts in folder: LLM can call via tool (e.g., run Python)

### Standardization
- Skills from open-source repos follow metadata format
- Parse metadata automatically for context

### LLM Caching
- Not covered in guided learning; instructor can share resources on request

## MCP and Custom Databases (e.g., Cloud SQL)
- MCP exposes API; does not know your schema
- **Describe tables and columns** in tool descriptions
- Add clarifications in MCP tool descriptions so LLM can form correct queries
- No manual system-prompt changes; runtime loads tools from MCP and includes descriptions

## Multi-Agent Architecture
- Agents run **async**; manager/lead agent coordinates
- Manager keeps connections open; sub-agents report when done
- Similar to ChatGPT Deep Research, Pro mode (background jobs, notifications)
- Same framework (e.g., LangChain) for single and multi-agent; coordination logic is manual
- System prompts used to avoid loops and long runs (e.g., Deep Research prompts)

## Distributing Tools Company-Wide via MCP
- Implement **MCP server** for your tool (e.g., DB comparison script)
- Add MCP server to chatbot (Cursor, Claude desktop, Codex)
- **No separate agent** needed; Claude/Cursor/Codex already act as agents
- Cursor: MCP config; Claude desktop: JSON config; Codex: add MCP servers in UI
