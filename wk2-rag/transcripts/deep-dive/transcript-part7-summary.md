# Deep Dive Part 7 Summary

## Q&A: RAG with SQL / Structured Data

### Insurance Claims Example
- Data in SQL tables; question: "Why are dental claims down?"
- **Embedding**: use SQL-specialized embedding models (e.g., fine-tuned on SQL); general-purpose may not work well
- **LLM**: 10B+ parameter models often handle SQL; no need for SQL-specialized LLM
- **Privacy**: local run = fully private; no data sent externally

## Q&A: Structured vs. Unstructured Data Retrieval

### Hybrid Retrieval
- Vector search + keyword/text search used together
- Hard to know a priori which to route to; often run both
- Retrieval is fast; not a bottleneck; optimize for accuracy

### Vector Index Concept
- Table: IDs + vectors (chunk → embedding mapping)
- FAISS: data structures for fast retrieval; inverse index for document ↔ vector mapping
- External services (e.g., Google): optimization at index layer; embedding model choice affects quality

## Q&A: Chunk Overlap

### Why Overlap Helps
- Reduces chance of splitting mid-sentence/paragraph
- Bad split → both chunks lose meaning; overlap provides redundancy
- Best practices: experiment; no universal rule

## Q&A: Fine-Tuning (LoRA, RAFT)

### Fine-Tuning in General
- Common when general LLM insufficient (coding, medical, custom style)
- Cost: less than pre-training; often days or weeks; small use case can be hours
- RAFT: RAG-specific; train LLM to handle noisy retrieved content; rarely used now (agents/thinking models handle it)

### Local Fine-Tuning
- Small models on powerful Mac: possible
- Beyond few billion params: usually needs cloud (e.g., Together, Replicate)

## Q&A: FAISS Persistence

### Storing Index
- FAISS advanced topics: how to persist and load; supports billions of vectors
- Not always in-memory; can write to storage
