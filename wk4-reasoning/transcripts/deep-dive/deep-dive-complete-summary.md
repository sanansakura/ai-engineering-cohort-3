# Deep-Dive Complete Summary

**Source:** Meeting transcript (Project 4 deep dive — deep research), 2/14/2026.

High-level overview: Session walks through Project 4 (building a simple deep-research system): inference-time scaling techniques (few-shot CoT, zero-shot CoT, self-consistency, sequential revision, tree of thought), inspecting a trained reasoning model (DeepSeek-R1), and implementing a deep-research agent with optional multi-agent extension. Q&A covers practice at labs, bootstrapping data, tooling/MCP, coding agents, evaluation, and security.

---

## Context and roadmap

### Project 5 (brief)
- Project 5 is released: multimodal agent (image/video generation) with a **router** that chooses language vs image/video generation.
- Image/video models are expensive (billions of parameters); **run on GPU** (e.g. Google Colab) recommended.

### Project 4: deep research
- **Deep research**: chatbots do thorough web study and return long reports (e.g. ChatGPT, Gemini). Project 4 builds a simpler version.
- Two ways to make models “think”: **inference-time scaling** (prompting/sampling, no weight change) vs **training** (SFT/RL to get reasoning).
- Roadmap: (1) Inference-time techniques with a non-reasoning model, (2) Inspect DeepSeek-R1, (3) Training reasoning models (pseudo-code/guided learning), (4) Build deep-research agent, (5) Optional multi-agent.

---

## Environment and setup

- **Environment**: Conda or UV; use **deep_research** kernel (not V3). UV preferred for speed.
- **Ollama**: Run `ollama serve` in a separate terminal. Pull: `llama3.2:3b`, `deepseek-r1:1.5b`, `qwen2.5:3b-instruct`.
- **Notebook**: OpenAI client with `base_url="http://localhost:11434/v1"` for Ollama.

---

## Inference-time scaling techniques

### Few-shot chain-of-thought

#### GPT-2
- **Completion model** (no instruction tuning); used to show effect of prompting.
- Hugging Face: `pipeline("text-generation", model="gpt2")`; optional `torch.float16`, `device="mps"` (Mac).
- Without few-shot: question alone → poor or no step-by-step reasoning.
- **Few-shot**: add examples in format “Steps: … Therefore, the answer is X” → GPT-2 follows format (quality limited by model size).

#### Llama 3.2
- Instruction-tuned; **already** does step-by-step reasoning.
- Few-shot used to **control format**, e.g. `[GIVEN]` / `[FIND]` / `[SOLVE]` / `[ANSWER]`.
- Messages: `role` and `content` (user/system/assistant).

### Zero-shot chain-of-thought
- Append **“Let’s think step by step”** to the question (from “Large language models are zero-shot reasoners”).
- No examples; often improves answers; widely used in practice.

### Self-consistency
- **Best-of-N sampling**: same prompt sent N times; pick best answer (e.g. **majority voting** on final answer).
- Often combined with CoT.
- **Implementation**: Prompt must ask for a **parseable final line**, e.g. “Therefore, the answer is &lt;number&gt;.” Use regex to extract answer. Loop N times (e.g. 5), collect answers; `collections.Counter(answers).most_common(1)` for winner. Optional: keep reasoning traces and return the trace that led to the winning answer.
- Higher temperature increases diversity; good when majority is correct but some runs are wrong.

### Sequential revision
- **Sequential** (vs parallel in self-consistency): generate draft → send draft + “evaluate and improve” → get new draft; repeat for `max_steps`.
- System prompt: “You are a helpful assistant, keep answers clear and correct.” Each round: original question + current draft + “Please revise, make clearer and more accurate. Only include the new answer.”
- Burns more inference compute; can fix mistakes across rounds.

### Tree of thought (ToT)

#### Concept
- Treat reasoning as **search**: maintain frontier of partial solutions; expand, **score**, **prune** (keep top-K); repeat until depth or goal.
- More efficient than generating many full chains then voting.

#### Word ladder (no LLM)
- Problem: transform word A → word B, one letter change per step, all in vocabulary.
- **neighbors(word, vocab)**: all words one character different and in vocab.
- **tree_of_thought(start, goal, vocab, max_depth, beam_width)**: frontier of paths; expand, sort by heuristic (e.g. edit distance to goal), keep top `beam_width`. Shows ToT as **algorithmic search**.

#### LLM-based ToT
- **propose_thought(question, state, k)**: prompt LLM to propose k next steps from current partial solution (state).
- **score_state(question, state)**: prompt LLM to score 1–10 “how promising”; parse number; fallback 5.
- **tree_of_thought(question, depth, width)**: frontier = list of (state, score); each step: expand with `propose_thought`, score new states, sort by score, keep top `width`; repeat until `depth`. Return best state/score.
- Same idea as word ladder but thoughts and scoring from LLM; “pro” style systems use search over solution tree.

---

## Training reasoning models (recap)

- Covered in guided learning: e.g. **STaR**, reinforcement learning; pseudo-code in project. DeepSeek-R1 is an example of a **trained** reasoning model.

---

## Inspecting a reasoning model (DeepSeek-R1)

- Same client pattern as Llama; model set to DeepSeek (e.g. smaller variant for speed).
- **No** “think step by step” in prompt; model was **trained** to produce thinking before answering.
- Output: **thinking tokens** (internal reasoning), then **final answer**. Code can split on `<think>...</think>` (or similar) to show thinking vs final answer.
- Inference can be slower than non-reasoning models of similar size because of long thinking.

---

## Building the deep-research agent

### Idea
- Deep research = **agent (LLM + tools)** + **reasoning-capable model** (or strong model). Same agent pattern as before; swap in a model that supports tool calling and reasoning.

### Implementation
- **Tool**: Web search via **DDGS** (DuckDuckGo); `@tool`, query → list of results → concatenate body/title into string.
- **Model**: e.g. `qwen2.5:3b-instruct` (must support **tool calling**; DeepSeek-R1 does not).
- **Agent**: LangChain `create_agent(llm, [ddg_search])`.
- Invoke: `agent.invoke({"messages": [{"role": "user", "content": question}]})`; print last message content.
- Flow: model reasons → calls search → gets snippets → reasons again → final answer.

---

## Optional: multi-agent deep research

- **Planner**: LLM decomposes query into 1–5 sub-questions.
- **Researchers**: each sub-question → search (DDGS) + summarize (e.g. one agent or function per sub-question).
- **Synthesizer**: single LLM call with all findings + original query → final report.
- `deep_research(query)`: plan → (parallel or sequential) research → synthesize.
- **In practice multi-agent is hard**: context sharing, when to use which tools, edge cases. “Don’t build multi-agent systems” article recommended for challenges and best practices. Solutions will be released.

---

## Q&A: Reasoning and models in practice

- **Do labs use inference-time scaling and reasoning models?** Yes: both. Example: one non-reasoning + one reasoning model; “pro” = reasoning model + search (best-of-N, sequential revision, tree search).
- **Choosing model vs inference compute (e.g. for a company):** Start with a small reasoning model (e.g. DeepSeek 1.5B), build eval set, measure. If weak: try better model or more inference compute. Trade-offs: cost per request, **latency** (reasoning and search add time).
- **Bootstrapping domain-specific reasoning data:** Manually create a **few** step-by-step examples. Few-shot prompt LLM to generate more → train on them → use model to generate more → filter/validate → retrain; repeat. See STaR-style / bootstrapping papers.
- **Synthetic data and licensing:** Using API/LLM output to train your model can violate licenses (distillation). Check provider terms; there have been discussions (e.g. DeepSeek vs OpenAI) about this.
- **ToT: same or different model for scoring vs proposing?** Can be same or different. In practice: use **smaller/cheaper model for scoring** when sufficient; **larger for proposing** if needed. Find smallest adequate model by testing.

---

## Q&A: Agents and tooling

- **When does the agent call a tool?** Model is constrained to **structured output**: when it wants to call a tool, it emits a specific format (e.g. special tokens or JSON). Runtime parses that, runs the tool, appends result to context, continues. Example: OpenAI harmony response format (e.g. “channel” for final vs tool call). It’s format/training, not free-form intent.
- **Tooling vs MCP:** Tools = list of callables (Python or MCP tool objects) passed to the agent. **MCP** = standardized protocol so agents can discover/use tools. Personal agents can be given high-level instructions (“search for skills, install when needed”); agent then finds and uses MCP/skills dynamically (e.g. OpenCLI-style).
- **Multi-agent and “super-agents”:** Multi-agent is difficult. “Super-agents” not clearly defined in session; instructor to follow up after reading.

---

## Q&A: Coding agents and evaluation

- **AI coding tools (determinism, methods):** Use **low temperature** for more deterministic code. **Agentic coding model**: LLM trained on code + **tool-use trajectories** (edit, run, read output). Tools: read file, edit file, run tests. Practice: generate unit tests, run via tools; if tests fail, model revises. Syntax: training on clean code (e.g. AST-filtered) and optionally **guided decoding** (constrain next token to valid syntax/structures).
- **Syntax and API correctness:** **Training**: heavy cleaning; **AST** used to filter invalid syntax. **Inference**: **guided decoding** (e.g. valid JSON, or tokens that don’t break syntax). Plus unit-test loop for runtime/semantic errors.
- **Models and tool use:** Models can be **bad at when to call which function**. E.g. “agents.md vs skills”: single static agents.md often outperforms modular skills because the model sometimes doesn’t invoke the right skill. Be careful with tool design and context.
- **Security and input validation:** Instructor to share links later (e.g. course portal) on best practices; inference vs system-prompt considerations.
- **Evaluating open-ended / deep-research tasks:** **Component-level**: evaluate retrieval, search, etc. with standard metrics/benchmarks. **End-to-end**: harder. For **coding**, unit tests help. For **novel reasoning** (e.g. science), evaluating correctness of traces is very hard; ongoing research (evals, benchmarks).

---

## Q&A: Inference-time techniques and “pro” models

- **Are CoT/self-consistency/etc. internalized in latest models?** Still debated. Even if internalized, **multiple attempts** (e.g. best-of-N) often help. “Pro” products combine reasoning model + extra inference-time compute; benchmarks often show pro on top.
- **Evals and cost:** Systems are complex; trade-offs (latency, cost, quality) are non-trivial; many recent efforts on evals (e.g. OpenAI, “real tiny evals”) and HVAC/real-world evals.

---

## Key takeaways

- **Inference-time scaling**: few-shot CoT, zero-shot CoT (“Let’s think step by step”), self-consistency (best-of-N + majority vote), sequential revision (draft → revise loop), tree of thought (search over partial solutions with propose + score).
- **Reasoning models**: e.g. DeepSeek-R1; trained to think before answering; output has thinking tokens then final answer.
- **Deep research**: agent (LLM + tools, e.g. DDGS search) with a reasoning-capable, tool-calling model; optional multi-agent (planner → researchers → synthesizer) is harder in practice.
- **Practice**: Labs use both reasoning models and inference-time scaling; start simple (small model + eval), then adjust model or compute; be careful with tool use and multi-agent design; coding agents use tool trajectories, low temperature, guided decoding, and unit-test loops.
