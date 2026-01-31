# Deep Dive Part 3 Summary

## Vector Store (FAISS)

### FAISS Overview
- Facebook AI Similarity Search; efficient nearest-neighbor at scale
- Build index from embeddings; search with k-nearest neighbors
- LangChain has wrapper: `FAISS.from_documents(chunks, embedding_model)`
- Handles: embedding chunks, creating index, storing vectors

### Saving and Loading
- `vector_db.save_local("faiss_index")` — creates `.pkl` and `index.faiss` files
- 42 embeddings stored
- Load at inference time instead of re-indexing

### Retrieval Object
- `vector_db.as_retriever(search_kwargs={"k": 8})` — top 8 most similar chunks per query
- Optional: `score_threshold` to discard distant results when query is outlier
- Retriever: wrapper with `get_relevant_documents(query)` etc.

## LLM (Ollama)

### Ollama Setup
- Local server: `ollama serve` (run in separate terminal)
- `ollama pull gemma2:1b` — pull model
- Many models available: Gemma (Google), Qwen, etc.

### Creating LLM
- `ChatOllama(model="gemma2:1b")` — simple API
- `llm.invoke("Hi, what is your name?")` — send requests
- Abstracts loading, tokenization, generation (vs. manual Hugging Face flow in Project 1)

## RAG Chain

### Components
- Retriever (from vector DB)
- LLM (Ollama)
- System prompt template with placeholders: `{context}`, `{question}`

### Template
- Static instructions + dynamic `context` (retrieved docs) and `question` (user)
- Python f-strings or `ChatPromptTemplate.from_template()` from LangChain
- Format at runtime: `prompt.format_messages(context=..., question=...)`
