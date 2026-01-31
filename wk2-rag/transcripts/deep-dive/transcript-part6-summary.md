# Deep Dive Part 6 Summary

## Q&A: Embedding Models vs. LLM Embedding Layers

### Why Dedicated Embedding Models?
- **Objective**: LLMs optimized for next-token prediction; embedding models for similarity
- LLM embedding layer: single lookup table; embedding models: full transformer with attention
- Embedding models almost always better for retrieval
- Size constraint is secondary; main reason is task optimization

### LLM Embeddings on Similarity Tasks
- No known papers comparing; intuition: not comparable to dedicated embedding models

## Q&A: RAG for Domain-Specific Knowledge

### Agents vs. Static RAG
- Community moved to agents post-Max (LLM); agents better for dynamic tasks
- Agents: LLM + tools (read files, run commands); coding agents = agents
- RAG for static knowledge; agents for interactive, tool-using workflows

## Q&A: Combining RAG, Fine-Tuning, Prompt Engineering

### Retrieval Is Universal
- Retrieval component used everywhere: RAG, agents, coding agents
- Fine-tune LLM for coding → put in agent → add retrieval for codebase
- Can combine retrieval with fine-tuned models

## Q&A: Vector Databases in Production

### Tools
- Instructor will share list of production tools on course portal
- Chroma, Qdrant, others mentioned

### Evaluation Libraries
- **Query expansion**: improve vague/grammatically imperfect queries
- **Guardrails**: input/output filtering; often LLM-based (fine-tuned or instructed)
- **Evaluation**: embedding metrics (recall, precision); LLM eval; end-to-end (LLM-as-judge)
- Open-source: OpenAI Evals; LangSmith for observability
