# Office Hours Transcript Part 2 Summary

## Post-course and fine-tuning

### After course ends
- Slack / Q&A may continue for a while
- Fine-tuning: consider when general model doesn't fit or for very niche use cases

## Agents preview (Week 3)

### Clubhouse / system agents
- Clubhouse: agents running on your system with full access
- **Difference from RAG:** RAG has published corpus; agents need "back channels" (e.g., Gmail, tools)
- **Tools:** Agents use tools to act (email, search, etc.)
- Foundation similar to RAG; "software layer on top of agent setup"

## Long context vs RAG

### When to use RAG vs long context
- **Long-context models:** Can attach lots of content; cost and performance considerations
- **Problem with long context:** Models drift or hallucinate beyond a certain length
- **RAG advantage:** Retrieve only relevant chunks; avoid context overload
- **Skills / folders:** Create separate prompts for different skills (support, analytics, etc.); agent loads only relevant skill into context

## Grounding and retrieval

### With long-context models (e.g., Rabbit)
- Less need to optimize retrieval when context is large
- If retrieval doesn't match, system drops non-matching parts and may re-retrieve

### Vector search vs keyword
- **Keyword / full-text search:** Traditional; no ML; exact or partial match
- **Vector search:** ML-based; embed query and chunks; semantic similarity
- **Modern systems:** Mostly use vector search; keyword rarely sufficient for complex queries

## Embedding and indexing

### Per-chunk embedding
- Embed each chunk separately, not the whole document
- Each chunk → embedding model → vector

### Document types (e.g., bank statement, driver's license)
- Index each document type into its own structure
- Cover all relevant fields per document type
