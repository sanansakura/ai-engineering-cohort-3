# Deep Dive Part 2 Summary

## Chunking

### Text Splitters
- LangChain text splitters: break documents into smaller, retrievable chunks
- **Recursive Character Text Splitter**: preferred; starts from largest semantically coherent chunks (paragraphs → sentences) until chunk size met
- **Length-based**: simpler but can break meaning mid-sentence
- **Chunk overlap**: improves retrieval; chunks share some content to avoid splitting important context

### Implementation
- `chunk_size=300`, overlap configured (guided learning has examples)
- `text_splitter.split_documents(raw_docs)` expects list of LangChain Document objects
- Result: 42 chunks from parsed PDFs
- Each chunk: same Document object, smaller `page_content`

## Indexing Options

### Vector vs. Text-Based
- **Vector-based**: common; good for vague/semantic queries
- **Text-based**: keyword search; good for specific terms, names, IDs
- **Hybrid**: often used in production

### Embedding Models
- Map text → high-dimensional vectors (e.g., 384 dimensions)
- Trained so similar meaning → nearby in embedding space
- Enables nearest-neighbor search for retrieval
- Hugging Face: load model, call `encode(sentences)`; LangChain supports many

### Sentence Transformers
- `HuggingFaceEmbeddings` with model name (e.g., small lightweight model)
- `embed_query("Hello World")` returns vector
- May need to switch to bigger models after evaluation for production
