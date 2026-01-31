# Office Hours Transcript Part 4 Summary

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

## Governance and explainability

### Healthcare / legal decisions
- **Past:** 94% accurate prediction but no explainability or auditability
- **Need:** Trace decisions back to factors, weights
- **Challenge:** Model can change over time → different answers
- **Direction:** Field working on governance platforms for traceability

## Watermarks and model security

### Watermarks
- Some companies add hidden watermarks to models
- No widely known techniques to guarantee model traceability in RAG/generation context
