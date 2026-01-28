# RAG Portfolio Deployment Plan — Consistency Review

This document reviews **RAG_PORTFOLIO_DEPLOYMENT_PLAN.md** for overall consistency, gaps (especially around document upload), and readiness for implementation.

---

## 1. Overall Consistency

- **Progress checklist, Plan of Work (Parts 1–4), and Concrete Steps (1.1–1.6, 2.x, 3.x)** are generally aligned. Parts 1–4 map to Steps 1.2–1.5; Agent 2/3 steps match the workflow.
- **Decision Log** is consistent with the plan (session-scoped uploads, configurable LLM, separate repo, multi-agent workflow).
- **Validation and Acceptance** criteria match the described behavior (local run, upload+index, configurable LLM, deployment).
- **Interfaces and Dependencies** list Streamlit/LangChain surface area used in the plan.

**Minor inconsistencies:**
- Plan uses `k=8` in Interfaces; `app.py` uses `RETRIEVAL_K=12`. Implementation should pick one (plan says 8; we can align to plan).
- Notebook uses "I'm not sure from the docs" / "I don't know based on the retrieved documents"; `app.py` uses a different refusal phrase. Plan says "I don't know based on the documents" in System prompt — small wording variance, acceptable.

---

## 2. Document Upload — Explicit vs Vague

### Where it *is* explicit
- **Step 1.3:** Clear instructions: add `st.file_uploader` (PDF, optionally TXT), an "Index" (or similar) action, load → chunk → embed → `FAISS.from_documents` → store in `st.session_state["vectordb"]` and `["retriever"]`, use session retriever when building the chain.
- **Validation — "Upload and index":** Describes the desired behavior (upload PDFs, click index, next questions use that retriever, no persistence after refresh).

### Where it is vague or implicit
1. **Purpose / Part 2:** Upload is described at a high level ("upload… chunked and indexed", "Provide a clear 'Index documents' or 'Use these documents' action") but without a step-by-step UI flow. Missing: *where* the control lives (sidebar vs top), *when* the Index button is enabled (e.g. only when files selected), and whether "Use these documents" is the same as "Index" or a separate action.
2. **"Use default docs" mode:** The Purpose says the app will offer a **"use default docs" mode"**. Part 3 and Step 1.4 describe a **fallback** when no upload exists (default corpus or pre-built index), but there is **no explicit UX**: no "Use default docs" button, toggle, or mode switch. The behavior is *implicit* (no upload → use default) rather than an explicit user choice. Implementers could reasonably add a toggle; the plan doesn’t require it.
3. **Placement:** "Sidebar or top section" / "sidebar or above chat" leaves layout under-specified. Fine for flexibility, but not a single prescribed layout.
4. **Optional TXT:** "Optionally TXT" appears in Purpose, Part 2, Step 1.3, and Interfaces. It’s never a dedicated sub-step (e.g. "Step 1.3b: Add TXT support") — easy to overlook or implement inconsistently.
5. **Clear chat after indexing:** Part 2 says *"After indexing, optionally clear or replace chat history so the next answers use the new context."* This is **not** in any Concrete Step. Easy to miss during implementation.
6. **Error handling:** Agent 2 is asked to review "missing files, empty uploads, index build failures" and "validate file types." The **development steps do not** explicitly say to validate file types, handle empty uploads, or show user-facing errors on index failure. So review expects it, but implementation steps don’t enumerate it.

---

## 3. Recommended Additions to the Plan

To make document upload **explicitly** outlined in steps:

1. **Add a "Document upload — explicit steps" subsection** (e.g. under Plan of Work or Concrete Steps) that spells out:
   - **UI:** `st.file_uploader` for PDF (and optionally `.txt`) in sidebar or dedicated section; accepted types and validation (e.g. reject non-PDF/non-TXT).
   - **Action:** A single "Index documents" (or "Use these documents") **button**, enabled only when at least one file is selected.
   - **On click:** For each uploaded file, load (PyPDFLoader / TextLoader) → append to `all_docs` → chunk with `RecursiveCharacterTextSplitter(300, 30)` → embed → `FAISS.from_documents` → store in session state; then (optionally) clear or replace chat history. On failure (e.g. corrupt PDF, empty file): show error message, do not overwrite session index.
   - **Switching:** Use session retriever when it exists; otherwise use default index. No separate "use default docs" toggle required unless we explicitly add it.

2. **Extend Step 1.3** (or add 1.3a/1.3b) with:
   - File type validation and handling of empty uploads.
   - User-visible error handling for load/chunk/index failures.

3. **Add optional Step** (or note in Part 2): "Optionally, clear chat history after indexing so the next answers use the new context."

4. **Clarify "use default docs" mode:** Either (a) define it purely as "fallback when no upload" (current implied behavior), or (b) add an explicit UI element (e.g. "Use default Everstorm docs" button) and a corresponding step.

---

## 4. Other Gaps

- **Retriever vs chain lifecycle:** Step 1.3 says "use session retriever if present; otherwise default." The plan doesn’t specify whether the **chain** is rebuilt when switching (default ↔ uploaded). `ConversationalRetrievalChain` takes the retriever at construction; switching retriever implies rebuilding the chain. Implementation should build the chain with the *current* retriever (default or session) whenever it’s used.
- **FilteredRetriever:** `app.py` uses `FilteredRetriever` to exclude BigCommerce docs. The plan doesn’t say whether **uploaded** docs should be filtered. Reasonable default: no filtering for user uploads; only default Everstorm index uses filtering.
- **`@st.cache_resource`:** Plan says use it "only for embedding model and other stateless objects; keep per-session index in session state." Step 1.3 echoes this. The current app caches the whole `load_chain()` result; we should refactor to cache only embeddings (and possibly LLM) and build chain per retriever.

---

## 5. Summary

| Area | Consistent? | Notes |
|------|-------------|--------|
| Progress ↔ Parts ↔ Steps | Yes | Same scope, clear Agent 1/2/3 roles |
| Document upload | Partially | Step 1.3 is explicit; Purpose/Part 2 vaguer; no explicit UI flow, error handling, or "clear chat" in steps |
| Default vs uploaded | Implicit | Fallback when no upload; no explicit "use default docs" **mode** in UX |
| Configurable LLM | Yes | Step 1.4 and Part 3 align |
| Deployment artifacts | Yes | requirements.txt, README, faiss_index/data |

**Recommendation:** Keep the plan as-is for overall structure, but add the **explicit document-upload steps** (and optional error-handling / clear-chat substeps) so that upload is unambiguously outlined and implementers don’t rely on vague phrasing.

---

*Review date: 2025-01-27. Plan reference: RAG_PORTFOLIO_DEPLOYMENT_PLAN.md.*
