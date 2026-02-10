# Office Hours Transcript Part 2 Summary

## Production Challenges: Nondeterminism and Context

### More Tools → More Nondeterminism
- More tools and components increase nondeterminism
- Highly governed environments make production deployment difficult
- Multi-agent systems: little evidence of successful, large-scale production use

### Context Window Growth
- Putting LLM in a loop causes context to grow with each tool result
- Performance degrades with large context (drift, forgetting middle content)

### Mitigation: File-Based Storage
- Store observations and results in files instead of keeping all in active memory
- Agent saves to markdown when no longer needed; tracks metadata (file locations)
- On demand: read relevant files back into context
- Combines with summarization/compaction techniques
- **Claude Code** uses this pattern (read/edit/save files)

## Agent as Orchestrator
- Agent does not decide which tool to use
- Agent watches LLM output; when format indicates tool call → parse → execute → append result
- Like MVC controller or orchestrator

## Multi-Agent: Who Decides?
- LLM is always the decision-maker
- Agent runtime is thin logic (~10 lines): send input, parse output, execute tools

## LLM’s Dual Role
- Predicts next token and predicts when tool call is needed
- Tool schema is always in context; LLM maps user intent to tools

## Walkthrough: GetWeather Example
- System prompt: “You have access to tool GetWeather”
- LLM produces: thought → tool_call GetWeather(SF) → agent stops generation → parses → executes → appends observation → sends back to LLM → LLM continues

## RAG and Agent Verification

### RAG Verification
- Use another LLM (often smaller) to check that output matches retrieved references

### Hallucination
- Retrieved content can be wrong; LLM verification doesn’t fix bad retrieval
- Tools (e.g., live search) reduce hallucination vs. static knowledge base

### Evaluation
- Benchmarks for hallucination; LLM-as-judge (compare output to ground truth)
- Verifiable domains (math, coding): run tests to check correctness

### User Feedback
- Thumbs up/down common (e.g., ChatGPT); detailed feedback rare
- Depends on product/PM; more feedback enables automated analysis

## React Across Domains
- Agent runtime is **generic**; LLM is replaceable black box
- **Tools** are domain-specific (coding: read/edit files, bash; other domains: different tools)
- Frameworks (e.g., LangChain) provide create_agent; add system prompt and tools

## Formats: React vs. Harmony
- OpenAPI **Harmony**: response format for tool calls; easier to parse
- GPT-4o models trained on Harmony; agent runtime must parse Harmony format
- React is one option; system prompt can define other formats

## Agency Levels
- **Multi-step agent** (single agent, multiple tool calls): most common in industry
- **Multi-agent**: e.g., ChatGPT Deep Research; coordinator + sub-agents; not yet widely productionized
