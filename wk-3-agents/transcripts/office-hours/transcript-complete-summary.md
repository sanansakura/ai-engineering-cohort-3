# Office Hours Complete Summary

This document summarizes the Week 3 agents office hours covering React, tool calling, agents vs. workflows, MCP, skills, memory, evaluation, and production considerations.

---

## Key Takeaways

- **React** is a prompting technique (think → act → observe) that frameworks implement under the hood.
- **Agents** give the LLM autonomy; workflows are static and developer-defined.
- **Agent runtime** orchestrates; the **LLM** decides and produces tokens; the LLM cannot call tools by itself.
- **Tools** are domain-specific; runtime and loop are generic across domains.
- **MCP** standardizes tool exposure; describe tools (e.g., DB schema) in tool descriptions.
- **Memory**: short-term = context; long-term = external storage retrieved on demand.

---

## React and the Agent Loop

### What React Is
- A **prompting technique** only—no training or fine-tuning
- Uses a system prompt with **think → act → observe** cycle and few-shot examples
- Frameworks (e.g., LangChain) implement this under the hood—no manual prompt creation needed
- **Reasoning LLMs** make the cycle stronger because they are trained to reason

### How It Works
- LLM receives system prompt + user query and produces tokens following the loop
- When an action is needed: produces a parseable format → agent runtime parses → executes tool → appends observation → sends back to LLM → LLM continues

### React vs. Other Formats
- **OpenAPI Harmony**: alternative response format for tool calls; easier to parse
- GPT-4o models are trained on Harmony; agent runtime must parse Harmony format
- React is one option; the loop matters more than the exact format

---

## Tool Calling

### Parameter Mapping
- LLM uses its understanding of words, concepts, and arguments
- With good function name, description, and inputs, it maps arguments to parameters
- Larger models (1B → 3B → 7B) handle tool calling much better
- Smaller models may fail on multiple simultaneous tool calls; larger models handle this

### How Tools Are Introduced
- **Manual**: introduce tools via schema to any LLM; works if the model is big enough
- **Trajectory training**: train on tool-calling examples; Palama, Qwen K2.5, and similar models use this

### Built-in vs. Custom Tools
- **GPT models**: trained on tools like web search, terminal, bash
- **Composer (Cursor)**: coding LLM fine-tuned on ~10+ tools (read/edit files, run commands)
- **Custom tools**: expose via MCP or other integration methods

### Tool Schema in Context
- Tool schema (function names, parameters, descriptions) is always in the LLM’s context
- LLM maps user intent to tools based on this schema

---

## Agent Runtime vs. LLM

### Agent Runtime (Orchestrator)
- Pure software; no ML, no parameters
- Coordinates LLM, tools, memory, and user I/O
- Does not think or produce tokens
- Parses tool calls from LLM output, executes tools, appends results to context
- Loads available tools (including MCP), sends them to the LLM as part of context

### LLM
- The “brain”; thinks, produces tokens, decides when to use tools
- Just a mathematical model (matrices); cannot call tools by itself
- Agent runtime is needed to bridge LLM output to tool execution

### Why an Agent Is Needed
- LLM alone cannot call tools; it only maps inputs to outputs
- Agent runtime implements the loop, tool execution, and context management

---

## Workflows vs. Agents

### Workflows
- **Static** graph; developer defines steps ahead of time
- Fixed sequence; no loop; LLM has no autonomy
- Can include multiple LLM calls but the flow is predetermined

### Agents
- **Dynamic**; agent decides next steps
- Autonomy: think → break task / call tools / produce final answer
- Agent runtime manages the loop; LLM makes the decisions

---

## Agent Types and Agency Levels

### create_react_agent, create_tool_calling_agent, create_agent
- Functionally similar; agents assume tools and a loop
- React describes the cycle; tools are separate; together they form an agent

### Multi-Step vs. Multi-Agent
- **Multi-step agent** (single agent, multiple tool calls): most common in industry
- **Multi-agent**: e.g., ChatGPT Deep Research; coordinator + sub-agents; harder to productionize
- Multi-agent systems are async; manager keeps connections open; sub-agents report when done

---

## MCP (Model Context Protocol)

### Purpose
- Standardize tool exposure across systems
- Reuse existing MCP servers instead of building tools from scratch

### Usage
- Agent loads tools from MCP servers and includes them in the LLM’s context
- To add tools: update config (e.g., `adjacent` file) with MCP server details

### Custom Databases (e.g., Cloud SQL)
- MCP exposes APIs; it does not know your schema
- **Describe tables and columns** in tool descriptions so the LLM can form correct queries
- Clarifications in MCP tool descriptions avoid manual system-prompt edits

### Distributing Tools Company-Wide
- Implement an **MCP server** for your tool (e.g., DB comparison script)
- Add it to the chatbot (Cursor, Claude desktop, Codex)
- No separate agent needed; the chatbot is already the agent

### MCP vs. Plugins
- Instructor noted the need to research plugins; MCP was covered in guided learning

---

## Skills (Markdown-on-File)

### Structure
- Skill = folder with `skill.md` (required), optional scripts, optional resources
- `skill.md` must include metadata: `name`, `description`

### Loading Flow
- Agent builds metadata (skill names + descriptions) and includes it in context
- LLM sees available skills; when needed, issues **open_file** with the skill path
- Agent loads `skill.md`, appends to context, LLM continues
- Scripts in the folder can be invoked via tools

### Standardization
- Open-source skill repos follow a consistent metadata format for parsing

---

## Memory

### Short-Term Memory
- Equals the **context window**
- Whatever is in context is what the LLM sees at each step

### Long-Term Memory
- Stored **outside** context
- Loaded on demand based on current input
- Examples: user preferences, retrieval from a knowledge base (RAG)

### Flow
- Long-term data is retrieved and **added to** short-term memory (context)

### Coding Agents
- Entire codebase stored externally (embedded, RAG-style)
- Retrieval fetches relevant chunks into context
- Codebase is too large to fit entirely in context

---

## Context Management and Production

### Context Growth
- Putting the LLM in a loop causes context to grow with each tool result
- Performance degrades with very large context (drift, forgetting middle content)

### File-Based Storage
- Store observations and results in files instead of keeping everything in active memory
- Agent saves to markdown when no longer needed; tracks metadata (file paths)
- On demand: read relevant files back into context
- Can be combined with summarization/compaction
- **Claude Code** uses this pattern

### Nondeterminism
- More tools and components increase nondeterminism
- Production deployment is harder in highly governed environments
- Multi-agent systems are difficult to productionize at scale

---

## Evaluation and Verification

### RAG Verification
- Use another LLM (often smaller) to check that output matches retrieved references

### Hallucination
- Retrieved content can be wrong; LLM verification does not fix bad retrieval
- Tools (e.g., live search) reduce hallucination compared with static knowledge bases

### Evaluation Methods
- Benchmarks for hallucination; **LLM-as-judge** (compare output to ground truth)
- Verifiable domains (math, coding): run tests (e.g., unit tests) to check correctness
- Semantic and context-based comparison, not word-for-word

### User Feedback
- Thumbs up/down common; detailed feedback is less common
- Product/PM decision; more feedback supports automated analysis (safety, hallucination, etc.)

---

## Input Format and Model Discovery

### JSON vs. Markdown
- Depends on model training
- **Markdown** preferred for most LLMs (system prompts often in markdown)
- **JSON** when appropriate (API payloads, coding artifacts)
- Do not convert JSON to markdown when it does not fit (e.g., DB query results)

### Hugging Face Hub
- Browse models at huggingface.co
- Example: search “Qwen K2”; use model page → “Use this model” → copy code
- Usage documented for Transformers, vLLM, and other backends

---

## Terminology

### AI Agent vs. Agentic AI Systems
- **AI agent**: wrapper around LLM + tools + loop (software you implement)
- **Agentic system**: broader system that includes agents and other components

### General Purpose vs. Domain-Specific LLMs
- Chatbots (ChatGPT, Gemini, etc.) use **general-purpose** LLMs
- Example: GPT 5.2 instant (non-thinking) and GPT 5.2 thinking

---

## Additional Notes

- **LLM caching**: not covered in guided learning; instructor can share resources on request
- **Multi-agent architecture**: similar to ChatGPT Deep Research and Pro mode (background jobs, notifications)
- **Codex**: supports adding MCP servers (local, HTTP, stdio) in the UI
