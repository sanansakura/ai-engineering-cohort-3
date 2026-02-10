# Week 3 Agents — One-Pager

Quick reference from the guided learning. For full detail, see `guided-learning-complete-summary.md`.

---

## What Are Agents?

**Agents = LLMs + autonomy + tools.** They plan, act, and adapt. Plain LLMs are next-token predictors; agents can complete multi-step tasks on behalf of users (e.g., legal research, phone calls, Codex fixing bugs, Operator browsing the web).

---

## The Agency Ladder

| Level | What It Is |
|-------|------------|
| **1. Single pass** | Prompt → LLM → response. Not really an agent. |
| **2. Workflows** | Fixed, predefined steps. No planning. |
| **3. Tool calling** | LLM can call functions (search, calculator, APIs). |
| **4. Multistep agents** | Dynamic plan–act–observe loop. Agent chooses steps. |

---

## Workflow Patterns (for fixed workflows)

- **Chunking:** Split complex tasks into subtasks → less error propagation.
- **Routing:** Router sends to specialized branch by intent (rule-based, ML, semantic).
- **Reflection:** Generate → Evaluate → Feedback → Regenerate loop; separate critic.
- **Parallelization:** Run independent steps in parallel (sectioning or voting).

---

## Tool Calling in 3 Steps

1. Define the function.  
2. Describe it to the LLM in the system prompt.  
3. Execute when the LLM outputs a tool call; append result to context and continue.

**MCP:** Anthropic’s Model Context Protocol. Service providers expose tools as servers; you connect via config instead of writing wrappers.

---

## Multistep Agents

**Loop:** Think → Act → Observe → repeat until done.

- **Plan, Act, Adapt:** Understand goal → plan → execute tools → get feedback → adjust.
- **ReAct:** Combines reasoning and acting in one loop.
- **Limitation:** Workflows lack live data and adaptivity; agents add both.

---

## Workflows vs Agents

| Workflows | Agents |
|-----------|--------|
| Predictable, fixed paths | Flexible, open-ended |
| Good for defined tasks | Good when steps are uncertain |
| Consistent, reliable | Can be slower, less stable |

---

## Multi-Agent Systems

Multiple agents work together. A **manager agent** coordinates and activates sub-agents. Challenges: coordination, communication, compounded errors. Need protocols (e.g., Agent2Agent) for discovery and messaging.

---

## Evaluation

- **Cost:** More steps → higher cost per request.  
- **Task success rate:** Benchmarks for specific domains.  
- **Frameworks:** LangChain, LangGraph for building agents.

---

## 8 Takeaways

1. Agents add planning, tools, and memory to LLMs.  
2. Agency ladder: single pass → workflows → tool calling → multistep.  
3. Use chunking, routing, reflection, parallelization for fixed workflows.  
4. Tool calling + MCP for standardized integration.  
5. Multistep agents: think–act–observe (e.g., ReAct).  
6. Multi-agent systems need manager + protocols.  
7. Workflows for predictable tasks; agents for open-ended ones.  
8. Track cost and task success; use frameworks for implementation.
