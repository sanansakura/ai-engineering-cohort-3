# Office Hours Transcript Part 1 Summary

## Session setup

### Week 2 format
- Q&A office hours for questions on project, guided learning, lectures
- Shared article: on-device LLMs, techniques to make models efficient (optional read)

### Capstone / project announcements
- Capstone dashboard: add projects for demo day
- Link to past cohorts' projects
- Both listed on main dashboard

## RAG system Q&A

### Chat history
- **What it is:** Previous conversation output fed as input to next turn
- **Example:** "Is it cool?" is vague without history; "How's the weather in San Francisco?" then "Is it cool?" needs context
- **Practice:** Include all previous turns in context each round; standard for chatbots in a session

### RAG evaluation
- Deep and important topic
- **For this project:** Can use ground truth (supervised output), compare model output
- **In practice:** Many companies may not need formal evaluation
- **RAGAS:** Has metrics; instructor can share references; "connecting the numbers"
- **End-to-end:** Evaluate entire system (relevant for agents too)

## Chunking and tables

### Tables split across chunks
- **Problem:** Table split into 2–3 chunks → embedded separately → may lose table structure when querying
- **Mitigation:** Use overlap between chunks
- **Chunk size:** Make it large enough for meaningful units; avoid splitting two different topics as one
- **Tuning:** Requires experiments and trial-and-error

### Document parsing
- **Simple docs:** Rule-based parsers more reliable and faster (less cost)
- **Complex layouts, images, multimedia:** Use Unstructured (or similar)
- **Chunking tools:** Ecosystem keeps changing; do research before choosing; LangChain includes many options

## Model and evaluation

### Model selection
- Use smallest model that delivers acceptable quality for users

### Evaluation best practice
- Have evaluation to understand impact on system quality
