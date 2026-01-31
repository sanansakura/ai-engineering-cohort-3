# Week 2 Office Hours — Complete Summary

Week 2 office hours covered RAG fundamentals, chunking, retrieval, evaluation, agents preview, governance, and logistics. This summary combines and merges themes from all parts while preserving every detail.

## Key takeaways

- **Chat history:** Include all previous turns in context each round; standard for chatbots
- **Chunking:** Use overlap; make chunk size large enough for meaningful units; avoid splitting tables or topics; tune via experiments
- **Parsing:** Rule-based for simple docs; Unstructured (or similar) for complex layouts/images
- **Retrieval:** Vector search is typical; hybrid top-k + distance threshold; RAGAS has reranking
- **Evaluation:** RAGAS metrics; ground-truth comparison; tune instructions before assuming model bias
- **Agents (Week 3):** Tools and back-channel access; foundation builds on RAG
- **Model:** Use smallest model that delivers acceptable quality

---

## Session setup and logistics

### Week 2 format
- Q&A office hours for questions on project, guided learning, lectures
- Shared article: on-device LLMs, techniques to make models efficient (optional read)

### Capstone / project announcements
- Capstone dashboard: add projects for demo day
- Link to past cohorts' projects
- Both listed on main dashboard

### Post-course
- Slack / Q&A may continue for a while after course ends

### Hands-on and feedback
- Request for more hands-on RAG practice
- Instructor open to sharing resources and references

---

## RAG fundamentals

### Chat history
- **What it is:** Previous conversation output fed as input to next turn
- **Example:** "Is it cool?" is vague without history; "How's the weather in San Francisco?" then "Is it cool?" needs context
- **Practice:** Include all previous turns in context each round; standard for chatbots in a session

### Long context vs RAG
- **Long-context models:** Can attach lots of content; cost and performance considerations
- **Problem with long context:** Models drift or hallucinate beyond a certain length
- **RAG advantage:** Retrieve only relevant chunks; avoid context overload
- **Skills / folders:** Create separate prompts for different skills (support, analytics, etc.); agent loads only relevant skill into context; useful when context is large

### Vector search vs keyword
- **Keyword / full-text search:** Traditional; no ML; exact or partial match
- **Vector search:** ML-based; embed query and chunks; semantic similarity
- **Modern systems:** Mostly use vector search; keyword rarely sufficient for complex queries

### Grounding with long-context models (e.g., Rabbit)
- Less need to optimize retrieval when context is large
- If retrieval doesn't match, system drops non-matching parts and may re-retrieve

---

## Chunking and indexing

### Tables split across chunks
- **Problem:** Table split into 2–3 chunks → embedded separately → may lose table structure when querying
- **Mitigation:** Use overlap between chunks
- **Chunk size:** Make it large enough for meaningful units; avoid splitting two different topics as one
- **Tuning:** Requires experiments and trial-and-error

### Document parsing
- **Simple docs:** Rule-based parsers more reliable and faster (less cost)
- **Complex layouts, images, multimedia:** Use Unstructured (or similar)
- **Chunking tools:** Ecosystem keeps changing; do research before choosing; LangChain includes many options

### Embedding and indexing
- **Per-chunk embedding:** Embed each chunk separately, not the whole document; each chunk → embedding model → vector
- **Document types (e.g., bank statement, driver's license):** Index each document type into its own structure; cover all relevant fields per document type

---

## Retrieval tuning

### Same question, same retrieval
- Yes: Same question → same retrieval cycle
- Retrieval is fast; not the bottleneck compared to generation

### When top-k misses the answer
- **Parameter 1:** Choose right similarity / max distance threshold
- **Parameter 2:** Value of k
- **Hybrid approach:** Retrieve top 10–20 chunks, then drop ones whose distance is too large (not relevant)
- **Tuning:** Try different k and threshold; evaluate what works

### Prompt caching
- **Concept:** New prompt = cache miss; if prefix already cached, reuse
- **OpenAI:** Prompt caching; splits prompt into blocks, caches; can save 80–90% of tokens
- Reference: OpenAI compression / prompt caching docs

### RAGAS
- Has metrics; includes reranking; instructor can share references; "connecting the numbers"

---

## Evaluation

### For this project
- Deep and important topic
- Can use ground truth (supervised output), compare model output
- In practice: Many companies may not need formal evaluation
- Evaluate entire system end-to-end (relevant for agents too)

### Model selection
- Use smallest model that delivers acceptable quality for users

### Evaluation best practice
- Have evaluation to understand impact on system quality

### LLM-as-judge and bias
- **Common cause:** Lack of precise instructions in system prompt, not model bias
- **If model bias:** Replace model
- **Limit:** Once you pick the best model for the task, little you can do about inherent bias

### Evaluation example (video search)
- Evaluate caption quality: scene, lighting, motion description accuracy

---

## Agents preview (Week 3)

### Clubhouse / system agents
- Clubhouse: agents running on your system with full access
- **Difference from RAG:** RAG has published corpus; agents need "back channels" (e.g., Gmail, tools)
- **Tools:** Agents use tools to act (email, search, etc.)
- Foundation similar to RAG; "software layer on top of agent setup"

---

## Fine-tuning

### When to consider
- When general model doesn't fit
- For very niche use cases

---

## Philosophical questions

### Feedback loops
- Systems depend on feedback loops
- **Input quality:** Manage high-quality input; some systems control prompt before embedding
- **Corpus / embedding space:** Who decides the corpus? Creates high-dimensional similarity space
- **Optimization:** Loss based on similarity; optimizer updates model so similar items are closer

### Developers and standardization
- Embedding/training is a "black box" for most developers
- Many developers experiment with their own tools
- Standardization still emerging

---

## Governance and explainability

### Healthcare / legal decisions
- **Past:** 94% accurate prediction but no explainability or auditability
- **Need:** Trace decisions back to factors, weights
- **Challenge:** Model can change over time → different answers
- **Direction:** Field working on governance platforms for traceability

### Watermarks and model security
- Some companies add hidden watermarks to models
- No widely known techniques to guarantee model traceability in RAG/generation context

---

## Tools and references

### LUNA and Quenmath
- **LUNA:** Variant or update related to LoRA
- **Quenmath:** Different focus; "core foundation is LoRA"
- LoRA variants evolving; check current docs

### Training LLM on org code
- **Question:** How to start training an LLM on company codebase
- **Answer:** Instructor to share references
- General approach: Use data that allows model to learn codebase; then iterate
