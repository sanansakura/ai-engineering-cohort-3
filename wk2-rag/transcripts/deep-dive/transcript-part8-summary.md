# Deep Dive Part 8 Summary

## Q&A: Multimodal RAG (Text, Images, Video)

### Indexing Modalities
- **Text + Images**: CLIP or similar shared embedding space
- **Video/Audio**: (1) embed directly with modality-specific models (BLIP, etc.), or (2) caption/transcript → text embedding (simpler)
- YouTube example: text-based search on transcripts/captions

### Video Chunking
- Long videos: chunk transcript or split video, caption each chunk, then embed

## Q&A: Web Search in Capstone

### Tool Calling
- Add web search as tool; covered in guided learning (agents)
- Project 3: introduce web search to LLM; LLM decides when to use it

## Q&A: Complex PDFs / Tables

### AI-Based Parsers
- Layout detection: bounding boxes, entity types (text, figure, table)
- Handle tables, images separately; extract text blocks with coordinates
- Instructor will share document parsing resources

## Q&A: Scaling RAG

### Indexing at Scale
- Don’t reindex everything; incrementally add new documents
- Reindex only when embedding model changes

### Retrieval at Scale
- Replace exact nearest neighbor with approximate nearest neighbor (FAISS supports)
- FAISS scales to billions of vectors

### Throughput
- Add GPUs; batch requests; distribute across GPUs (e.g., RunAI, vLLM)
- LLM is bottleneck; embedding/retrieval usually not
- May switch to smaller models for cost/latency

## Q&A: Document Parsing Evaluation

### Metrics
- Bounding box metrics (IoU, etc.); classification accuracy for entity types
- End-to-end evaluation: instructor will read more and follow up
