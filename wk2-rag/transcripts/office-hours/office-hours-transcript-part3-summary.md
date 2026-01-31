# Office Hours Transcript Part 3 Summary

## Retrieval behavior

### Same question, same retrieval
- Yes: Same question → same retrieval cycle
- Retrieval is fast; not the bottleneck compared to generation

### Prompt caching
- **Concept:** New prompt = cache miss; if prefix already cached, reuse
- **OpenAI:** Prompt caching; splits prompt into blocks, caches; can save 80–90% of tokens
- Reference: OpenAI compression / prompt caching docs

## Top-k and relevance

### When top-k misses the answer
- **Parameter 1:** Choose right similarity / max distance threshold
- **Parameter 2:** Value of k
- **Hybrid approach:** Retrieve top 10–20 chunks, then drop ones whose distance is too large (not relevant)
- **Tuning:** Try different k and threshold; evaluate what works

### RAGAS
- Includes reranking

## LLM-as-judge and bias

### Bias in evaluation
- **Common cause:** Lack of precise instructions in system prompt, not model bias
- **If model bias:** Replace model
- **Limit:** Once you pick the best model for the task, little you can do about inherent bias

### Evaluation example (video search)
- Evaluate caption quality: scene, lighting, motion description accuracy
