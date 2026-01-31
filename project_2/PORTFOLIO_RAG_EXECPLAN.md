# Portfolio-Ready Interactive RAG Chatbot with Multi-Agent Development Workflow

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept in date as work proceeds.

This document must be maintained in accordance with PLANS.md located at the repository root.

## Purpose / Big Picture

After this implementation, you will have a production-ready, portfolio-quality RAG (Retrieval-Augmented Generation) chatbot that employers can interact with directly. The system will allow users to upload their own documents (PDFs, text files, markdown), which will be automatically indexed and made searchable through an intelligent chat interface. The project demonstrates advanced RAG capabilities including document ingestion, semantic search, context-aware generation, and citation tracking. The entire development process will be automated using a three-agent workflow (Developer, Reviewer, Orchestrator) with git worktrees, minimizing manual intervention while ensuring code quality and project alignment.

Visitors to your portfolio will be able to: upload documents, ask questions about their content, receive accurate answers with source citations, see real-time indexing progress, and experience a polished, professional interface that showcases your full-stack AI engineering skills. The system will be deployed on Streamlit Cloud or Hugging Face Spaces, making it immediately accessible without any setup required.

## Execution Autonomy

**CRITICAL: Once execution commences, the process must continue autonomously through all phases and steps until completion.**

This ExecPlan is designed for autonomous execution from start to finish using a three-agent workflow. The implementing agents must:

1. **Execute Continuously**: Once Phase 1 begins, proceed immediately to Phase 2, then Phase 3, and so on through all 7 phases without stopping for approval or confirmation between phases.

2. **Three-Agent Workflow Per Step**: For EACH step in the implementation, the following workflow MUST be followed:
   - **Step A: Developer Agent** writes and implements the code according to the step requirements
   - **Step B: Reviewer Agent** reviews the code for quality, style, correctness, and best practices
   - **Step C: Orchestrator Agent** reviews the implementation to ensure it aligns with overall project goals, checks for consistency with previous steps, and approves merging
   - Only after all three agents have completed their work for a step should the process proceed to the next step

3. **Complete All Steps**: Every step within each phase must be completed (including all three agent workflows) before moving to the next phase. Do not skip steps or phases, even if intermediate validation passes.

4. **Resolve Issues Autonomously**: If errors occur during implementation, agents must attempt to resolve them using available tools (codebase search, web research, trial and error) before requesting assistance. Only stop if a blocking issue cannot be resolved after reasonable attempts.

5. **Update Progress Continuously**: As each step completes (after all three agents have finished), immediately update the Progress section with timestamps and checkboxes. Do not wait until the end to document progress.

6. **Maintain Living Document**: Update the Decision Log, Surprises & Discoveries, and other living document sections in real-time as work proceeds, not retrospectively.

7. **Final Validation**: Only after all phases are complete should final validation and acceptance testing occur. The system must be fully functional and deployed before considering the plan complete.

**The goal is a fully working, deployed portfolio application with zero manual intervention required during execution.**

## Progress

- [ ] (YYYY-MM-DD HH:MMZ) Project initialization and repository setup
- [ ] (YYYY-MM-DD HH:MMZ) Git worktree structure created for multi-agent workflow
- [ ] (YYYY-MM-DD HH:MMZ) Core RAG infrastructure implemented (document loading, chunking, embedding)
- [ ] (YYYY-MM-DD HH:MMZ) Vector database integration (FAISS/ChromaDB) with persistence
- [ ] (YYYY-MM-DD HH:MMZ) Document upload and indexing UI implemented
- [ ] (YYYY-MM-DD HH:MMZ) Interactive chat interface with citation tracking
- [ ] (YYYY-MM-DD HH:MMZ) Multi-agent development workflow implemented
- [ ] (YYYY-MM-DD HH:MMZ) Deployment configuration for Streamlit Cloud/Hugging Face
- [ ] (YYYY-MM-DD HH:MMZ) Testing and validation completed
- [ ] (YYYY-MM-DD HH:MMZ) Documentation and README finalized

## Surprises & Discoveries

(To be populated during implementation)

## Decision Log

### Decision: Interactive Document Upload Over Pre-loaded Content
**Rationale:** Employers want to see the system's capabilities firsthand. Allowing document upload demonstrates: (1) real-time document processing, (2) dynamic indexing capabilities, (3) handling of diverse document types, (4) user-centric design. Pre-loaded content limits engagement and doesn't showcase the full technical stack.
**Date/Author:** 2026-01-25 / ExecPlan Author

### Decision: Multi-Agent Workflow with Git Worktrees
**Rationale:** Git worktrees allow parallel development branches in separate directories without switching contexts. This enables: (1) Developer agent works in `worktree-dev/`, (2) Reviewer agent works in `worktree-review/`, (3) Orchestrator manages merges in main worktree. This pattern minimizes conflicts and allows true parallelization of code review and development.
**Date/Author:** 2026-01-25 / ExecPlan Author

### Decision: Streamlit Cloud as Primary Deployment Target
**Rationale:** Streamlit Cloud offers: (1) free hosting for public repos, (2) automatic deployments from GitHub, (3) built-in environment management, (4) easy sharing via URL. Alternative: Hugging Face Spaces for broader ML community visibility. Both support requirements.txt and can handle FAISS/embedding models.
**Date/Author:** 2026-01-25 / ExecPlan Author

### Decision: FAISS over ChromaDB for Vector Storage
**Rationale:** FAISS is: (1) battle-tested and performant, (2) works well with LangChain, (3) supports local persistence, (4) already used in project_2. ChromaDB offers better metadata filtering but adds complexity. For portfolio, FAISS demonstrates core competency without unnecessary complexity.
**Date/Author:** 2026-01-25 / ExecPlan Author

### Decision: Three-Agent System Architecture
**Rationale:** 
- **Developer Agent**: Implements features, writes code, creates PRs. Focus: functionality and implementation.
- **Reviewer Agent**: Reviews code quality, checks style, validates tests, suggests improvements. Focus: quality and maintainability.
- **Orchestrator Agent**: Manages PRs, ensures alignment with project goals, handles merges, coordinates agents. Focus: project coherence and workflow.
This separation ensures each agent has clear responsibilities and prevents conflicts.
**Date/Author:** 2026-01-25 / ExecPlan Author

## Outcomes & Retrospective

(To be populated upon completion)

## Context and Orientation

The current project_2 contains a basic RAG chatbot implementation (`app.py`) that works with pre-loaded Everstorm PDF documents. The system uses FAISS for vector storage, LangChain for orchestration, and Streamlit for the UI. The existing codebase provides a foundation but lacks: (1) document upload capability, (2) dynamic indexing, (3) production-ready deployment configuration, (4) automated development workflow.

Key files in the current implementation:
- `project_2/app.py`: Main Streamlit application (380 lines, modernized with type hints)
- `project_2/rag_chatbot.ipynb`: Jupyter notebook with document processing pipeline
- `project_2/faiss_index/`: Pre-built FAISS vector index
- `project_2/data/`: Sample PDF documents
- `project_2/environment.yml`: Conda environment specification

The new portfolio project will be created in a separate directory structure to maintain separation from the educational project_2. The portfolio project will be self-contained, deployable, and showcase-ready.

Terms used in this plan:
- **RAG (Retrieval-Augmented Generation)**: A technique where an LLM generates answers using information retrieved from a knowledge base, reducing hallucinations.
- **Vector Database**: A database that stores documents as high-dimensional vectors (embeddings) for semantic similarity search.
- **Git Worktree**: A feature allowing multiple working directories for the same repository, each checking out different branches.
- **Streamlit Cloud**: A hosting platform that automatically deploys Streamlit apps from GitHub repositories.
- **FAISS**: Facebook AI Similarity Search, a library for efficient similarity search in high-dimensional spaces.

## Plan of Work

The implementation will proceed in distinct phases, each building upon the previous. The work will be organized using git worktrees to enable parallel agent workflows.

**Execution Model: Autonomous Continuous Execution with Three-Agent Workflow**

This plan must be executed continuously from Phase 1 through Phase 7 without interruption. Each phase builds upon the previous, and the three-agent system must work together for each step:

**Workflow Pattern for Each Step:**
1. **Developer Agent** implements the code according to step specifications
2. **Reviewer Agent** reviews the code for:
   - Code quality and style
   - Correctness and functionality
   - Best practices and maintainability
   - Test coverage
   - Documentation completeness
3. **Orchestrator Agent** ensures:
   - Implementation aligns with overall project goals
   - Consistency with previous steps and architecture
   - Integration points are properly handled
   - Project structure and conventions are maintained
   - Code is ready for merge and next step

**Execution Rules:**
- Complete all three agent workflows for each step before proceeding to the next step
- Complete all steps in Phase N (with full three-agent workflow) before beginning Phase N+1
- Validate each phase's completion before proceeding
- Update progress tracking in real-time after each step completes
- Continue execution even if minor issues arise (resolve autonomously)
- Only stop if a truly blocking issue occurs that cannot be resolved

The phases are designed to be executed sequentially in a single continuous session. Do not pause between phases for approval or confirmation. The entire implementation should proceed autonomously until the portfolio application is fully deployed and functional.

**Phase 1: Project Foundation and Structure**
Create a new portfolio project directory structure separate from project_2. Set up git worktrees for the three-agent workflow. Initialize the core application structure with proper configuration management, logging, and error handling. This phase establishes the foundation that all subsequent work builds upon.

**Phase 2: Core RAG Infrastructure**
Implement document loading for multiple formats (PDF, TXT, MD), intelligent text chunking with overlap, embedding generation using a production-ready model, and vector database creation with FAISS. This phase creates the engine that powers document understanding and retrieval.

**Phase 3: Document Upload and Dynamic Indexing**
Build the Streamlit UI components for file upload, implement background processing for document indexing, create progress indicators, and handle multiple document uploads. This phase enables the interactive experience that makes the portfolio piece engaging.

**Phase 4: Interactive Chat Interface**
Develop the chat UI with message history, implement the RAG query pipeline with citation tracking, add source document visualization, and create a polished, professional interface. This phase creates the user-facing experience that demonstrates the system's capabilities.

**Phase 5: Multi-Agent Development Workflow**
Implement the three-agent system using a workflow orchestration framework. Create agent definitions with specific roles, set up git worktree management, implement PR creation and review automation, and build the orchestrator that coordinates merges and ensures project alignment. This phase automates the development process.

**Phase 6: Deployment and Production Readiness**
Configure the application for Streamlit Cloud deployment, create requirements.txt with pinned versions, set up environment variables, write comprehensive README documentation, and add usage examples. This phase makes the project accessible to employers and portfolio viewers.

**Phase 7: Testing and Validation**
Create test suites for document processing, RAG pipeline, and UI components. Implement integration tests, validate the multi-agent workflow, and perform end-to-end testing. This phase ensures reliability and demonstrates software engineering best practices.

Each phase will be implemented incrementally with validation checkpoints. The multi-agent workflow will be introduced in Phase 5, but earlier phases will use standard git workflow to establish the codebase.

**Important**: After completing each phase (with all steps having gone through the three-agent workflow), immediately proceed to the next phase. Do not wait for external approval or confirmation. The validation checkpoints are for the agents to verify correctness, not stopping points for human review. Continue execution through all phases until the complete system is deployed and functional.

**Three-Agent Workflow Reminder**: For every step in every phase, ensure the Developer Agent writes code, the Reviewer Agent reviews it, and the Orchestrator Agent validates alignment before moving to the next step.

## Concrete Steps

**Execution Note**: Execute all steps in sequence using the three-agent workflow. For EACH step:

1. **Developer Agent** implements the code according to the step requirements
2. **Reviewer Agent** reviews the code for quality, correctness, and best practices
3. **Orchestrator Agent** validates alignment with project goals and approves proceeding

Only after all three agents complete their work for a step should you proceed to the next step. Complete Step 1 (with full three-agent workflow), then immediately proceed to Step 2, and continue through all steps until the entire system is implemented and deployed. Update the Progress section after completing each step (after all three agents finish), but do not pause execution between steps once the workflow is complete.

### Step 1: Create Portfolio Project Structure

**Three-Agent Workflow for This Step:**
- Developer Agent: Creates the directory structure and initial files
- Reviewer Agent: Reviews structure for best practices, checks for missing components
- Orchestrator Agent: Validates structure aligns with project goals and sets foundation correctly

Working directory: `/Users/tempUser/Projects/ai-engineering-course`

Create a new directory for the portfolio project:

    mkdir -p portfolio-rag-chatbot
    cd portfolio-rag-chatbot
    git init
    git remote add origin <your-github-repo-url>  # Set this to your actual repo

Create the initial directory structure:

    mkdir -p src/{core,ui,agents,utils}
    mkdir -p tests/{unit,integration}
    mkdir -p docs
    mkdir -p data/uploads
    mkdir -p .streamlit

Create initial files:

    touch README.md
    touch requirements.txt
    touch .gitignore
    touch .streamlit/config.toml
    touch src/__init__.py
    touch src/core/__init__.py
    touch src/ui/__init__.py
    touch src/agents/__init__.py
    touch src/utils/__init__.py

Expected result: A clean project structure ready for development.

### Step 2: Set Up Git Worktrees for Multi-Agent Workflow

**Three-Agent Workflow for This Step:**
- Developer Agent: Creates git worktrees and branch structure
- Reviewer Agent: Reviews git setup for correctness and workflow efficiency
- Orchestrator Agent: Validates worktree structure supports the three-agent workflow properly

Working directory: `/Users/tempUser/Projects/ai-engineering-course/portfolio-rag-chatbot`

Create worktrees for each agent:

    # Main worktree (orchestrator's workspace)
    git checkout -b main
    git commit --allow-empty -m "Initial commit"

    # Developer worktree
    git worktree add ../portfolio-rag-chatbot-dev develop
    git checkout -b develop

    # Reviewer worktree  
    git worktree add ../portfolio-rag-chatbot-review review
    git checkout -b review

Expected result: Three separate directories, each with their own branch checked out:
- `portfolio-rag-chatbot/` (main branch, orchestrator)
- `../portfolio-rag-chatbot-dev/` (develop branch, developer agent)
- `../portfolio-rag-chatbot-review/` (review branch, reviewer agent)

### Step 3: Implement Core Document Processing

**Three-Agent Workflow for This Step:**
- Developer Agent: Implements DocumentProcessor class with loading and chunking functionality
- Reviewer Agent: Reviews code for error handling, type hints, documentation, and best practices
- Orchestrator Agent: Validates implementation aligns with RAG architecture and integrates properly with vector store

Working directory: `/Users/tempUser/Projects/ai-engineering-course/portfolio-rag-chatbot`

Create `src/core/document_processor.py`:

    from typing import List
    from pathlib import Path
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.schema import Document
    import logging

    logger = logging.getLogger(__name__)

    class DocumentProcessor:
        """Handles document loading and chunking for RAG system."""
        
        def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
            self.chunk_size = chunk_size
            self.chunk_overlap = chunk_overlap
            self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len
            )
        
        def load_document(self, file_path: Path) -> List[Document]:
            """Load a document based on its file extension."""
            suffix = file_path.suffix.lower()
            
            if suffix == '.pdf':
                loader = PyPDFLoader(str(file_path))
            elif suffix in ['.txt', '.md']:
                loader = TextLoader(str(file_path))
            else:
                raise ValueError(f"Unsupported file type: {suffix}")
            
            return loader.load()
        
        def process_document(self, file_path: Path) -> List[Document]:
            """Load and chunk a document."""
            docs = self.load_document(file_path)
            chunks = self.splitter.split_documents(docs)
            
            # Add metadata
            for chunk in chunks:
                chunk.metadata['source_file'] = file_path.name
                chunk.metadata['source_path'] = str(file_path)
            
            logger.info(f"Processed {file_path.name}: {len(docs)} pages -> {len(chunks)} chunks")
            return chunks

Create `src/core/vector_store.py`:

    from typing import List, Optional
    from pathlib import Path
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import SentenceTransformerEmbeddings
    from langchain.schema import Document
    import logging

    logger = logging.getLogger(__name__)

    class VectorStore:
        """Manages FAISS vector store for document embeddings."""
        
        def __init__(self, index_path: str = "vector_index", embedding_model: str = "thenlper/gte-small"):
            self.index_path = Path(index_path)
            self.embeddings = SentenceTransformerEmbeddings(model_name=embedding_model)
            self.vectordb: Optional[FAISS] = None
        
        def create_index(self, documents: List[Document]) -> None:
            """Create a new FAISS index from documents."""
            logger.info(f"Creating index with {len(documents)} documents")
            self.vectordb = FAISS.from_documents(documents, self.embeddings)
            self.save_index()
        
        def add_documents(self, documents: List[Document]) -> None:
            """Add documents to existing index."""
            if self.vectordb is None:
                self.load_index()
            
            if self.vectordb is None:
                self.create_index(documents)
            else:
                self.vectordb.add_documents(documents)
                self.save_index()
        
        def save_index(self) -> None:
            """Save the index to disk."""
            if self.vectordb is not None:
                self.index_path.mkdir(parents=True, exist_ok=True)
                self.vectordb.save_local(str(self.index_path))
                logger.info(f"Index saved to {self.index_path}")
        
        def load_index(self) -> bool:
            """Load index from disk. Returns True if successful."""
            if (self.index_path / "index.faiss").exists():
                self.vectordb = FAISS.load_local(
                    str(self.index_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info(f"Index loaded from {self.index_path}")
                return True
            return False
        
        def get_retriever(self, k: int = 4):
            """Get a retriever from the vector store."""
            if self.vectordb is None:
                self.load_index()
            
            if self.vectordb is None:
                raise ValueError("No index available. Please upload and index documents first.")
            
            return self.vectordb.as_retriever(search_kwargs={"k": k})

Expected result: Core document processing and vector storage functionality implemented and testable.

### Step 4: Implement Streamlit UI with Document Upload

**Three-Agent Workflow for This Step:**
- Developer Agent: Implements Streamlit UI components for file upload and chat interface
- Reviewer Agent: Reviews UI code for user experience, error handling, and code quality
- Orchestrator Agent: Validates UI integrates properly with core components and meets portfolio showcase requirements

Working directory: `/Users/tempUser/Projects/ai-engineering-course/portfolio-rag-chatbot`

Create `src/ui/app.py`:

    import streamlit as st
    from pathlib import Path
    import tempfile
    import os
    from typing import List
    from src.core.document_processor import DocumentProcessor
    from src.core.vector_store import VectorStore
    from src.core.rag_chain import RAGChain
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Page configuration
    st.set_page_config(
        page_title="Interactive RAG Chatbot",
        page_icon="🤖",
        layout="wide"
    )

    # Initialize session state
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = VectorStore()
        st.session_state.vector_store.load_index()
    
    if "rag_chain" not in st.session_state:
        if st.session_state.vector_store.vectordb is not None:
            retriever = st.session_state.vector_store.get_retriever()
            st.session_state.rag_chain = RAGChain(retriever)
        else:
            st.session_state.rag_chain = None
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar for document upload
    with st.sidebar:
        st.header("📄 Document Management")
        
        uploaded_files = st.file_uploader(
            "Upload documents (PDF, TXT, MD)",
            type=["pdf", "txt", "md"],
            accept_multiple_files=True
        )
        
        if st.button("Process & Index Documents"):
            if uploaded_files:
                processor = DocumentProcessor()
                all_chunks = []
                
                with st.spinner("Processing documents..."):
                    for uploaded_file in uploaded_files:
                        # Save uploaded file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_path = Path(tmp_file.name)
                        
                        try:
                            chunks = processor.process_document(tmp_path)
                            all_chunks.extend(chunks)
                            st.success(f"✅ Processed {uploaded_file.name}: {len(chunks)} chunks")
                        except Exception as e:
                            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
                        finally:
                            os.unlink(tmp_path)
                
                if all_chunks:
                    with st.spinner("Indexing documents..."):
                        st.session_state.vector_store.add_documents(all_chunks)
                        retriever = st.session_state.vector_store.get_retriever()
                        st.session_state.rag_chain = RAGChain(retriever)
                    st.success(f"✅ Indexed {len(all_chunks)} chunks. Ready to chat!")
            else:
                st.warning("Please upload at least one document.")
        
        # Show indexed document count
        if st.session_state.vector_store.vectordb is not None:
            st.info(f"📚 Documents indexed and ready")

    # Main chat interface
    st.title("🤖 Interactive RAG Chatbot")
    st.markdown("Upload documents and ask questions about their content. Answers include source citations.")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message:
                with st.expander("📚 Sources"):
                    for source in message["sources"]:
                        st.write(f"- {source}")

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        if st.session_state.rag_chain is None:
            st.warning("⚠️ Please upload and index documents first.")
        else:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        result = st.session_state.rag_chain.query(prompt)
                        response = result["answer"]
                        sources = result.get("sources", [])
                        
                        st.markdown(response)
                        
                        if sources:
                            with st.expander("📚 Sources"):
                                for source in sources:
                                    st.write(f"- {source}")
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response,
                            "sources": sources
                        })
                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

Expected result: A functional Streamlit app with document upload and chat interface.

### Step 5: Implement RAG Chain with Citations

**Three-Agent Workflow for This Step:**
- Developer Agent: Implements RAGChain class with query processing and citation tracking
- Reviewer Agent: Reviews RAG implementation for prompt engineering, citation accuracy, and error handling
- Orchestrator Agent: Validates RAG chain integrates with vector store and UI, and produces portfolio-quality results

Create `src/core/rag_chain.py`:

    from typing import Dict, List
    from langchain.chains import ConversationalRetrievalChain
    from langchain_community.llms import Ollama
    from langchain.prompts import PromptTemplate
    from langchain_core.retrievers import BaseRetriever
    import logging

    logger = logging.getLogger(__name__)

    SYSTEM_PROMPT = """You are a helpful AI assistant that answers questions based on the provided context from uploaded documents.

Rules:
1. Use ONLY the information from the context to answer.
2. If the answer is not in the context, say "I don't have enough information to answer this question based on the uploaded documents."
3. Be concise, accurate, and cite specific information when possible.
4. If multiple documents are relevant, synthesize information from all of them.

Context:
{context}

Question: {question}

Answer:"""

    class RAGChain:
        """Manages the RAG query pipeline with citation tracking."""
        
        def __init__(self, retriever: BaseRetriever, model: str = "gemma2:2b", temperature: float = 0.1):
            self.retriever = retriever
            self.llm = Ollama(model=model, temperature=temperature)
            
            prompt = PromptTemplate(
                template=SYSTEM_PROMPT,
                input_variables=["context", "question"]
            )
            
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=retriever,
                combine_docs_chain_kwargs={"prompt": prompt},
                return_source_documents=True,
                verbose=False
            )
        
        def query(self, question: str, chat_history: List = None) -> Dict:
            """Query the RAG system and return answer with sources."""
            if chat_history is None:
                chat_history = []
            
            result = self.chain.invoke({
                "question": question,
                "chat_history": chat_history
            })
            
            # Extract sources
            sources = []
            if "source_documents" in result:
                for doc in result["source_documents"]:
                    source_file = doc.metadata.get("source_file", "Unknown")
                    if source_file not in sources:
                        sources.append(source_file)
            
            return {
                "answer": result["answer"],
                "sources": sources,
                "source_documents": result.get("source_documents", [])
            }

Expected result: RAG chain implementation with source citation tracking.

### Step 6: Create Requirements and Deployment Configuration

**Three-Agent Workflow for This Step:**
- Developer Agent: Creates requirements.txt, config files, and deployment configuration
- Reviewer Agent: Reviews dependencies for security, version compatibility, and deployment readiness
- Orchestrator Agent: Validates configuration supports deployment targets and ensures production readiness

Create `requirements.txt`:

    streamlit>=1.28.0
    langchain>=0.1.0
    langchain-community>=0.0.20
    langchain-core>=0.1.0
    faiss-cpu>=1.7.4
    sentence-transformers>=2.2.2
    pypdf>=3.17.0
    pydantic>=2.0.0

Create `.streamlit/config.toml`:

    [theme]
    primaryColor = "#1f77b4"
    backgroundColor = "#ffffff"
    secondaryBackgroundColor = "#f0f2f6"
    textColor = "#262730"
    font = "sans serif"

Create `.gitignore`:

    __pycache__/
    *.pyc
    *.pyo
    *.pyd
    .Python
    vector_index/
    data/uploads/*
    !data/uploads/.gitkeep
    .streamlit/secrets.toml
    *.log
    .env
    venv/
    env/
    .pytest_cache/
    .coverage
    htmlcov/

Create comprehensive `README.md` with setup instructions, features, and usage examples.

Expected result: Project is ready for deployment to Streamlit Cloud.

### Step 7: Implement Multi-Agent Workflow System

**Three-Agent Workflow for This Step:**
- Developer Agent: Implements base agent classes and agent-specific implementations
- Reviewer Agent: Reviews agent code for proper abstraction, error handling, and workflow logic
- Orchestrator Agent: Validates agent system enables the three-agent workflow and integrates with git worktrees properly

Create `src/agents/base_agent.py`:

    from abc import ABC, abstractmethod
    from typing import Dict, Any
    import subprocess
    from pathlib import Path

    class BaseAgent(ABC):
        """Base class for development agents."""
        
        def __init__(self, name: str, worktree_path: Path):
            self.name = name
            self.worktree_path = worktree_path
        
        @abstractmethod
        def execute_task(self, task_description: str) -> Dict[str, Any]:
            """Execute a task and return results."""
            pass
        
        def run_git_command(self, command: str, cwd: Path = None) -> str:
            """Run a git command in the worktree."""
            if cwd is None:
                cwd = self.worktree_path
            
            result = subprocess.run(
                command.split(),
                cwd=cwd,
                capture_output=True,
                text=True
            )
            return result.stdout

Create `src/agents/developer_agent.py`, `src/agents/reviewer_agent.py`, and `src/agents/orchestrator_agent.py` with specific implementations for each agent's role.

Expected result: Three-agent system that can autonomously develop, review, and merge code.

## Validation and Acceptance

To validate the complete system:

1. **Document Upload Test**: Upload a PDF document, verify it processes and indexes correctly. Expected: Success message showing chunk count.

2. **Query Test**: Ask a question about the uploaded document. Expected: Accurate answer with source citations.

3. **Multi-Document Test**: Upload multiple documents, ask a question spanning multiple sources. Expected: Synthesized answer citing multiple sources.

4. **Deployment Test**: Deploy to Streamlit Cloud, verify public URL works. Expected: Accessible application with full functionality.

5. **Multi-Agent Workflow Test**: Trigger a development task, verify agents create PRs, review, and merge. Expected: Automated workflow completes without manual intervention.

Run the application locally:

    cd portfolio-rag-chatbot
    pip install -r requirements.txt
    streamlit run src/ui/app.py

Expected: Application starts on http://localhost:8501 with upload interface and chat functionality.

## Idempotence and Recovery

All steps can be repeated safely. The vector index is stored persistently, so re-running indexing will add to existing index. Git worktrees can be recreated if needed. If deployment fails, check Streamlit Cloud logs and requirements.txt compatibility.

## Artifacts and Notes

(To be populated during implementation with code snippets, test outputs, and deployment URLs)

## Interfaces and Dependencies

**DocumentProcessor** (src/core/document_processor.py):
- `load_document(file_path: Path) -> List[Document]`
- `process_document(file_path: Path) -> List[Document]`

**VectorStore** (src/core/vector_store.py):
- `create_index(documents: List[Document]) -> None`
- `add_documents(documents: List[Document]) -> None`
- `get_retriever(k: int) -> BaseRetriever`

**RAGChain** (src/core/rag_chain.py):
- `query(question: str, chat_history: List) -> Dict[str, Any]`

**BaseAgent** (src/agents/base_agent.py):
- `execute_task(task_description: str) -> Dict[str, Any]`

