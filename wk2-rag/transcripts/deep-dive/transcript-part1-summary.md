# Deep Dive Part 1 Summary

## Introduction and Context

### Week 3 Overview
- Deep dive of Project 2 (RAG chatbot)
- Week 3 content released: includes agents (instructor's favorite week)
- Transition from RAG (static) to more capable agent-based systems
- Project 3: build "Ask the Web" agent similar to Perplexity for tool calling

### Project 3 Preview
- Three parts: environment YAML, requirements.txt, assets (diagrams)
- Optional MCP section added for connecting MCP tools to LLM
- Switching to latest LangChain versions in Project 3 (Project 2 uses simpler older versions)
- UV package manager option: significantly faster than Conda; both supported

### RAG Architecture Recap
- RAG = LLM + retrieval system
- Retrieval: given documents (PDFs, images), finds relevant chunks for the query, passes to LLM
- Knowledge store = documents unique to company/use case

## Environment Setup

### Kernel and Dependencies
- Use `rag_chatbot` kernel (or equivalent environment)
- Verify: `langchain-community` version 0.3.24
- Skip environment setup section if already installed

## Use Case: Customer Support Chatbot

### Data
- Four Everstorm PDFs: payment/refund/security, product sizing/care, return/exchange, shipping/delivery
- Toy example; in practice: hundreds of PDFs, images, larger scale

### Indexing Pipeline
1. **Parse** documents (different loaders for PDF, HTML, etc.)
2. **Chunk** into semantically meaningful smaller pieces
3. **Index**: convert text → numerical vectors via embedding model → store in index
4. **Retrieve** at query time using the index

### Document Loading (LangChain)
- PyPDFLoader for PDFs; search LangChain docs for latest loaders (APIs change)
- `raw_docs`: list of PDF paths; load with `PyPDFLoader(path).load()`
- Result: 8 PDF pages from 4 files
- Optional: WebBaseLoader for URLs (same pattern, different loader)
- Fallback handling recommended when loading fails
