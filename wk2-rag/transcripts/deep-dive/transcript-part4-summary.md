# Deep Dive Part 4 Summary

## RAG Workflow Implementation

### Step-by-Step
1. **Retrieve**: `docs = retriever.get_relevant_documents(question)` — top 8 chunks
2. **Format docs**: extract `page_content` from each doc, join with `\n\n`
3. **Format prompt**: `prompt.format_messages(context=formatted_docs, question=question)`
4. **Generate**: `answer = llm.invoke(messages)`

### Optional: Citations
- Return `{"answer": ..., "source_documents": docs}` for grounding

### When Answer Is Wrong
- Inspect retrieved docs: was relevant chunk retrieved?
- If not: improve embedding model or retrieval
- If yes: LLM made a mistake; consider larger LLM or better prompting
- Retrieval (FAISS) is trusted; focus on embedding model and LLM

## Testing

### Sample Questions
- Refund policy, return process
- Shipping time
- Contact support
- Correct chunks retrieved → accurate answers
- Example: "What is the quickest way to contact support?" → correctly cites Everstorm logistics

## Streamlit UI (Optional)

### Packaging
- Same logic: vector DB, embedding model, LLM, optional chat history
- Gradio/Streamlit for UI
- `streamlit run app.py` to launch

## Recommendations

### Models
- **LLM**: Gemma 1B is minimal; prefer 3B or 7B for real apps
- **Embedding**: small model used; consider Ollama embedding models or larger Sentence Transformers

### Next Project
- UI: Chainlit instead of Streamlit (better for LLM/agent apps)
- Link: chainlit.io
