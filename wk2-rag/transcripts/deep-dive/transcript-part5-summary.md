# Deep Dive Part 5 Summary

## Q&A: Images in PDFs

### Extracting Images
- Two-phase AI-based parsers: (1) predict bounding boxes + entity types (text, figure, image); (2) extract items to structured output
- LangChain may support; specialized parsers exist for complex layouts
- Standalone image files: load directly with image loaders

### Embedding Images
- **Option 1**: Multimodal embedding model (e.g., CLIP) — shared space for text and images; embed both, store in same index
- **Option 2**: Image → caption (vision model) → text embedding model; keeps text-only pipeline
- CLIP: contrastive pre-training; maps text and images to shared embedding space

## Q&A: Embedding Model Architecture

### How Embedding Models Work
- Similar to LLMs: transformer-based, tokenizer, embedding layers
- Smaller than LLMs (simpler task)
- Training objective: similarity (similar inputs → similar embeddings), not next-token prediction

### Embedding vs. LLM Independence
- Embedding model is fully independent of LLM in RAG
- Retrieval returns text chunks, not vectors; LLM only sees text
- No parity concern between embedding model and LLM

## Q&A: Google Colab
- Project 2 can run locally or on Colab
- Colab: need to configure Ollama; search for how to expose Ollama on Colab
- Local: easier for Ollama setup
