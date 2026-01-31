# Deep Dive Part 9 Summary

## Q&A: Embedding Model Interoperability

### Switching Embedding Models
- No way to convert old embeddings to new model's space
- Must reindex when changing embedding model
- Reindexing cost is often negligible (small knowledge bases, GPUs)

## Q&A: RAFT Details

### RAFT Training
- Fine-tune LLM with noisy retrieved content; train to discard irrelevant chunks
- Replace LLM in RAG; no automation changes

## Q&A: Multiple Indexes / Databases

### Vector Database Choice
- Depends on content; software-engineering trade-offs
- Purpose-built vector databases (Pinecone, etc.) for production

## Q&A: System Prompt Size and Token Cost

### Cost
- Larger prompts = more tokens = higher cost (LLM processes all)
- Balance: enough context for accuracy, avoid unnecessary detail

### Agent Skills
- Dynamic loading: store expertise in files; agent loads relevant skills when needed
- Avoid massive static system prompt; used by OpenAI, Anthropic, etc.

## Q&A: Uploaded PDFs in Chat

### Behavior
- PDF content appended to context; not added to knowledge base
- New session: no access to previously uploaded PDF
- Memory: conversation history; retrieval from past conversations for recall

## Q&A: Document Update Frequency

### Reindexing
- Depends on use case, budget, compute
- ~90% of cases: reindex when content changes
- Minor additions: index only new content
- Do updates offline; test before rollout

## Q&A: Fine-Tuning vs. RAG Decision

### When to Fine-Tune
- Custom domain knowledge (e.g., medical)
- Behavior/style changes (shorter answers, tone)
- Inject knowledge the model doesn’t have

### When to Use RAG
- Data can be retrieved and provided as context
- Avoid fine-tuning cost when possible

## Q&A: Project Dependencies

### Per-Project Environments
- Each project independent; own environment YAML
- Project 3: newer LangChain, MCP, etc.
- UV: faster setup (~30 seconds)

## Q&A: AI Solution Lifecycle Management

### Tooling
- No known end-to-end platform for library/dependency lifecycle
- Manual monitoring; evaluate migrations case by case

## Q&A: Vector Store for Large Scale

### FAISS and Persistence
- FAISS docs cover persistence; supports very large indexes

## Q&A: Replacing Specific Documents

### Index Mapping
- Inverse index: document ↔ vectors
- Metadata + mapping allow updating specific document’s vectors

## Q&A: Production Deployment

### Swapping Components
- Replace Ollama with vLLM for production serving
- Use production-grade vector DB
- FastAPI or similar for API layer
- Deployment links in repo

## Q&A: Context and Question in Prompt

### Template Variables
- `context` and `question` filled at runtime
- Context = retrieved docs; question = user input
- RAG step formats message before sending to LLM
