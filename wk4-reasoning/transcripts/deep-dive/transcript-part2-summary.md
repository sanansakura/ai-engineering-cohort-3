# Deep-Dive Part 2 Summary

## Inspecting a reasoning model (DeepSeek-R1)

### Behavior
- Same client pattern as Llama; switch model to DeepSeek (e.g. smaller variant for speed).
- No “think step by step” in prompt; model was **trained** to produce thinking before answering.
- Output: **thinking tokens** (internal reasoning), then **final answer** (user-facing).
- Code can split content on `<think>...</think>` (or similar) to show “thinking” vs “final answer.”
- Thinking can be long; inference slower than non-reasoning models of similar size.

## Building the deep-research agent

### Idea
- Deep research = **agent (LLM + tools)** + **reasoning model** (or strong model).
- Same agent pattern as before; swap in a reasoning-capable model.

### Implementation
- **Tool**: web search via DDGS (DuckDuckGo); `@tool`, query → list of results → concatenate body/title into string.
- **Model**: e.g. `qwen2.5:3b-instruct` (must support tool calling).
- **Agent**: LangChain `create_agent(llm, [ddg_search])`.
- Invoke: `agent.invoke({"messages": [{"role": "user", "content": question}]})`; print last message content.
- Flow: model reasons → calls search → gets snippets → reasons again → final answer.

## Optional: multi-agent deep research

### Design
- **Planner**: LLM decomposes query into 1–5 sub-questions.
- **Researchers**: each sub-question → one agent (or function) that searches (DDGS) and summarizes.
- **Synthesizer**: single LLM call with all findings + original query → final report.
- `deep_research(query)`: plan → parallel or sequential research → synthesize.
- Solutions will be released; multi-agent is harder in practice (context sharing, tool use, edge cases).
- Reference: “Don’t build multi-agent systems” (article on challenges and when to avoid).

## Q&A: Reasoning and models in practice

### Do labs use inference-time scaling and reasoning models?
- Yes: inference-time scaling (multiple samples, search) **and** reasoning models (think-then-answer).
- Example: one non-reasoning + one reasoning model; “pro” often = reasoning model + search (e.g. best-of-N, sequential revision, tree search).

### Choosing model vs inference compute (e.g. for a company)
- Start simple: small reasoning model (e.g. DeepSeek 1.5B), eval set, measure.
- If model is weak: try better model or more inference compute (multiple samples, revision, search).
- Trade-offs: cost per request, latency (reasoning and search add time).

### Bootstrapping domain-specific reasoning data
- **Bootstrapping**: manually create a **few** step-by-step examples in your domain.
- Few-shot prompt an LLM to generate more such examples → train on them → use model to generate more → filter/validate → retrain; repeat.
- Not “insane” to scale; key is starting with a small seed and iterating (see STaR-style papers).

### Synthetic data and licensing (distillation)
- Using API/LLM output to train your own model can violate some licenses (distillation).
- Some providers have restricted or investigated this (e.g. reports about DeepSeek and OpenAI); check licenses.

### ToT: same or different model for scoring vs proposing?
- Can be same or different. In practice: use **smaller/cheaper model for scoring** when possible; use **larger model for proposing** if needed. Choose by task and testing.

## Q&A: Agents and tooling

### Multi-agent and “super-agents”
- Multi-agent is difficult (context, tool use, conflicts). “Super-agents” not clearly defined in session; may overlap with multi-agent; instructor to follow up after reading.

### Tooling vs MCP
- **Tools**: list of callables (Python functions or MCP tool objects) passed to the agent.
- **MCP**: standardized protocol so agents can discover/use tools in a common way.
- Personal agents can be given high-level instructions (“search for skills, install when needed”); agent then finds and uses MCP/skills dynamically (e.g. OpenCLI-style use cases).

### When does the agent call a tool?
- Model is constrained to **structured output**: when it wants to call a tool, it emits a specific format (e.g. special tokens or JSON). The runtime parses that, runs the tool, appends result to context, continues generation.
- Example: OpenAI harmony response format (e.g. “channel” for final vs tool call). It’s format/training, not free-form “intent” detection.

## Q&A: Coding agents and evaluation

### AI coding tools (determinism, methods)
- **Temperature**: low (e.g. 0) for more deterministic, syntax-friendly code.
- **Agentic coding model**: LLM trained on code + **tool-use trajectories** (edit, run, read output). Tools: read file, edit file, run tests, etc.
- Practice: generate unit tests, run them via tools; if fail, model revises. Syntax enforced by training (clean code, AST-filtered data) and optionally **guided decoding** (constrain next token to valid syntax/structures).

### Syntax and API correctness
- **Training**: heavy data cleaning; AST used to filter out invalid syntax so model sees only valid code.
- **Inference**: **guided decoding** can restrict output (e.g. valid JSON, or tokens that don’t break syntax). Plus unit-test loop to catch runtime/semantic errors.

### Latency/cost and tool use
- Models can be **bad at when to call which function**; e.g. “agents.md vs skills” finding: single static agents.md often works better than modular skills because model sometimes doesn’t invoke the right skill. Be careful with tool design and context.

### Security and input validation
- Instructor to share links later (e.g. via course portal) on best practices for security and validation; inference vs system-prompt considerations.

### Evaluating open-ended / deep-research tasks
- **Component-level**: evaluate retrieval, search, etc. with standard metrics/benchmarks.
- **End-to-end**: harder; for coding, unit tests help. For novel reasoning (e.g. science), evaluating “correctness” of traces is very hard; ongoing research (evals, benchmarks).

## Q&A: Inference-time techniques and “pro” models

### Are CoT/self-consistency/etc. internalized in latest models?
- Still debated; even if much is internalized, **multiple attempts** (e.g. best-of-N) often improve results. “Pro” products combine reasoning model + extra inference-time compute (search, multiple samples). Benchmarks often show pro variants on top.

### Evals and cost trade-offs
- Systems are complex; trade-offs (latency, cost, quality) are non-trivial; many recent efforts on evals (e.g. OpenAI) and real-world evals.

## Wrap-up

- Project 4 deep dive: inference-time scaling, DeepSeek inspection, deep-research agent, optional multi-agent.
- Next: project 5 (image/video, multimodal agent); see you next week.
