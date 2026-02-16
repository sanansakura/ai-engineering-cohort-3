---
name: transcript-summarizer
description: Splits transcript files into ~10-line chunks, generates hierarchical bullet summaries for each chunk, then produces a unified final summary. Use when the user wants to summarize a transcript, process office-hour recordings, review-session transcripts, or create structured summaries from long text files.
---

# Transcript Summarizer

Processes long transcript files by chunking, summarizing each chunk with hierarchical bullets, then synthesizing a unified final summary.

## Workflow

```
Transcript → Split (~10 lines/chunk) → Summarize each chunk (hierarchical bullets) → Unified final summary
```

## Step 1: Split transcript into chunks

Run the split script:

```bash
python .cursor/skills/transcript-summarizer/scripts/split_transcript.py <transcript_path> [--output-dir <dir>] [--chunk-size 10]
```

- **Input**: Path to transcript file (.txt)
- **Output**: Chunk files `transcript-part1.txt`, `transcript-part2.txt`, ... in `--output-dir` (default: same dir as input)
- **Chunk size**: ~10 lines (configurable)

If the script isn't available, split manually: read the file, split by newlines into groups of ~10, write each group to `transcript-partN.txt`.

## Step 2: Summarize each chunk

For each chunk file, create a summary with **hierarchical bullets**:

**Structure:**
- `# Chunk N Summary` (or `# [Source Name] Part N Summary`)
- `##` for major themes/topics
- `###` for subtopics
- `####` for fine-grained points
- Use `-` for bullet items under each heading

**Guidelines:**
- Capture key ideas, decisions, Q&A, instructions, and takeaways
- Preserve technical terms, names, and references
- Keep bullets concise; one idea per bullet
- Note transitions between topics

**Output:** Save as `transcript-partN-summary.md` alongside each chunk (or in a `summaries/` subdir).

**Example hierarchy:**
```markdown
## Topic Name

### Subtopic
- Key point
- Key point

### Another subtopic
- Key point
```

## Step 3: Unified final summary

Using all chunk summaries, create a **single coherent document** that combines, deduplicates, and merges themes — **without losing any context or details** from the part summaries.

**Approach:**
- **Combine:** Bring all content from part summaries into one document
- **Reduce redundancies:** When the same idea appears in multiple chunks, state it once; consolidate repeated points into a single, complete statement
- **Merge themes:** Group related topics across chunks into unified sections (e.g., all chunking content under one heading, all evaluation content under another)
- **Preserve everything:** Every substantive point, technical term, reference, tool name, command, decision, or instruction from the parts must appear in the final summary — either merged with similar points or as its own bullet
- **No omission:** Do not drop details to shorten; combine and merge instead of cutting

**Structure:**
- `# [Source] Complete Summary`
- High-level overview (2–3 sentences)
- Major sections organized by **theme** (not chunk order)
- Hierarchical bullets within sections
- Cross-reference themes that appear in multiple chunks

**Guidelines:**
- Order by logical flow, not chunk order
- Add a brief "Key takeaways" or "Summary" at top if helpful
- When merging, prefer the more complete or specific wording; include any unique detail from each occurrence
- Verify: every part-summary point has a home in the final document

**Output:** Save as `[source-name]-complete-summary.md` in the same directory as the transcript or summaries.

## Output locations

| File | Location |
|------|----------|
| Chunks | Same dir as transcript: `transcript-part1.txt`, etc. |
| Chunk summaries | Same dir: `transcript-part1-summary.md`, etc. |
| Final summary | Same dir: `[basename]-complete-summary.md` |

## Reference examples

In this repo:
- `project_1/review-session/` — part summaries + `review-session-complete-summary.md`
- `wk2-rag/guided-learning/` — part summaries + `transcript-complete-summary.md` (in transcripts folder)
