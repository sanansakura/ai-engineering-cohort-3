# Week 4 Guided Learning — Thinking and Reasoning Models: Complete Summary

This lecture covers reasoning models end-to-end: what they are, how to build them via inference-time scaling and training-time approaches, how to evaluate and guide reasoning with reward models, how to enable self-correction, how to internalize search into the model itself, and how all of these come together in practical applications like deep research. The course project (Project 4) is building a "deep research light" system.

---

## 1. What Are Reasoning Models?

### Definition and Core Concepts
- Reasoning models are LLMs that generate intermediate reasoning traces (a "thinking" phase) before producing a final answer
- The reasoning process is typically multi-step and can involve multi-path exploration — the model may try different reasoning directions
- Once thinking is complete, the model produces its final response
- Most top-performing models today are reasoning models

### Reasoning vs Non-Reasoning Models
- **Naming convention (OpenAI)**: Models starting with "o" (o3, o3 pro, o4 mini) are reasoning models; models starting with numbers (GPT-4o, GPT-4.5, GPT-4.1) are not
- Non-reasoning models may still exhibit some reasoning behavior (because their training data includes step-by-step examples) but are not specialized for it
- Reasoning models pause to "think" before responding; non-reasoning models respond immediately

### Live Demos Comparing Models
- **GPT-4o (non-reasoning)**: Responded instantly to a counting task with no thinking; gave an inaccurate answer
- **o4 mini (reasoning)**: Paused ~9 seconds to think; produced a more accurate, considered answer
- **o3 (more capable reasoning)**: Took over a minute to think; generated many more reasoning tokens; most thorough but most expensive
- OpenAI does not show the actual reasoning traces — displayed "thoughts" are summarized/reworded, not raw tokens
- Some platforms (e.g., Hyperbolic) do show the exact tokens generated during thinking

### Practical Model Selection Guidance
- **o4 mini**: Fast, efficient for day-to-day tasks; recommended default for most reasoning needs
- **o3**: For complex tasks requiring more reliable, thorough responses
- **o3 pro**: For very complex tasks where reliability is paramount
- Max tokens should be increased (e.g., to 10,000) when using reasoning models due to the volume of thinking tokens generated

### Notable Models on Leaderboards
- Anthropic's Claude Opus 4 is a high-capability reasoning model
- Kimi K2 by Moonshot ranked #5 on LM Arena despite being a non-thinking model from a smaller company — uses a modified MIT license
- GPT-4.5 and Claude Sonnet 4 rank highly despite not being reasoning models
- Alibaba's QWen models are also competitive
- LM Arena (Chatbot Arena) provides rankings across all models

---

## 2. Inference-Time Scaling Techniques

The core idea: spend more compute generating tokens at inference time to improve output quality — without changing the model's parameters.

### 2.1 Chain-of-Thought (CoT) Prompting

#### Few-Shot CoT
- Add worked examples in the prompt context showing step-by-step reasoning for similar questions
- Example: show "2 boxes with 3 balls each → 2 × 3 = 6 → Answer: 6", then ask the actual question
- The model follows the demonstrated reasoning pattern
- Providing more examples further guides the model

#### Zero-Shot CoT
- Based on "Large Language Models are Zero-Shot Reasoners" paper
- Simply append "Let's think step by step" to the prompt — no examples needed
- Works because training data already contains many step-by-step reasoning examples
- The paper provides comprehensive evaluations across different domains

#### Visualization
- Input → Thought 1 → Thought 2 → ... → Thought N → Final Answer
- Each thought is an intermediate reasoning step (e.g., "2 × 7 = 14")
- In practice, each thought may combine text description with computation

#### Demo with LLaMA 3
- Without CoT: model failed a math question entirely (wrong answer, wrong interpretation)
- With few-shot CoT example: model performed calculations correctly and arrived at the right answer (29 items)
- Demonstrates how prompting alone can push non-reasoning models to reason

### 2.2 Self-Consistency (Parallel Sampling / Best-of-N)

#### Core Idea
- Generate N complete responses in parallel (each with its own chain-of-thought reasoning) and pick the best one
- Also known as "parallel sampling" or "best-of-N sampling"
- Full control over compute budget: more samples = more tokens = better chance of a correct answer
- Evaluations show self-consistency consistently outperforms single-generation CoT across multiple domains

#### Picking the Best Response

**Majority Voting**
- Compare the N final answers; pick the one the majority agree on
- Works well for tasks with verifiable correct answers (math, factual questions)

**Reward Model Scoring**
- For subjective/open-ended tasks (writing, creative work), majority voting doesn't apply since all answers may be different but valid
- Use a reward model trained on human-scored prompt-response pairs
- The reward model assigns a quality score to each generation; pick the highest-scored one
- Enables self-consistency across any domain as long as the reward model covers it

### 2.3 Tree of Thoughts (ToT)

#### How It Works
- Treat text generation as a tree search problem
- Generate several intermediate reasoning steps from a given point
- Score each intermediate step; expand the most promising paths; prune low-scoring branches
- Continue dynamically: the best path with the highest cumulative score forms the final output

#### ToT vs Self-Consistency
- More focused on efficiency — instead of generating many full parallel branches, ToT is smarter about which directions to invest compute in
- Prunes bad directions early, saving compute for promising paths

#### Beyond ToT
- Many more search-based approaches exist (beam search, MCTS, etc.)
- A key paper evaluates parallel sampling, various search strategies, tree of thoughts, and advanced search methods
- Results show significant accuracy improvements, especially in math domains

### 2.4 Sequential Revision

#### How It Works
- Instead of parallel exploration, sequentially extend computation
- Pass the model its own previous output (prompt + CoT + response) and ask it to revise/improve
- Repeat for k iterations — each pass refines the answer

#### When to Use Parallel vs Sequential
- **Sequential**: Better for easier/medium difficulty questions — a single revision pass can fix simple mistakes
- **Parallel**: Better for complex/difficult questions — diverse exploration has a higher chance of finding the right approach
- Sequential revision risks getting stuck in the same wrong direction; parallel sampling explores diverse paths

### Summary of Inference-Time Scaling
- All techniques trade off inference-time compute for better outputs without changing model parameters
- Core principle: let the model think in different ways before committing to a final answer
- Techniques can be combined (e.g., CoT + self-consistency, ToT + reward models, sequential + parallel)

---

## 3. Training-Time Approaches for Reasoning

### 3.1 Fine-Tuning on Chain-of-Thought Data

#### Data Generation Process
1. Start with an LLM not capable of generating CoT reasoning
2. Use CoT prompting to elicit reasoning traces from the model
3. Generate multiple outputs via parallel sampling; identify correct answers
4. Correct question + reasoning trace pairs become training examples
5. Fine-tune the model on this CoT data
6. The improved model generates better CoT data for the next round — iterate

#### Special Tokens for Thinking
- Define special tokens to delineate reasoning from final output: `<think>` (token ID 128798) and `</think>` (token ID 128799)
- Training data format: Question → `<think>` reasoning steps `</think>` → Final Answer
- After fine-tuning, the model learns when to enter thinking mode, reason, then produce the answer

#### Key Insight
- Even non-reasoning models (e.g., GPT-4) have been trained on data containing CoT intermediate steps
- These models learn to generate some reasoning naturally from their training data
- This is why even non-reasoning models sometimes show reasoning behavior

### 3.2 Outcome Reward Modeling (ORM)

#### How ORM Works
- Training data: prompt + intermediate reasoning steps + final answer + label/score
- The score indicates how accurate the final answer is
- For verifiable tasks (math, coding), scoring can be automated by checking the final answer
- Train a reward model (a copy of the LLM with a scoring head) to predict this score
- Use the reward model to continue training the LLM — reinforcing responses that score well

#### Limitation
- ORM only scores the final answer — it completely ignores intermediate reasoning steps
- Incorrect intermediate steps go undetected as long as the final answer is correct
- The model may learn some implicit correlations, but feedback on intermediate steps is indirect

### 3.3 Process Reward Modeling (PRM)

#### How PRM Differs from ORM
- PRM scores each intermediate reasoning step individually, not just the final answer
- Each step in the chain gets its own correctness score
- More granular feedback: can identify exactly where reasoning goes wrong

#### Advantages
- Better visibility into the reasoning process
- More capable as verifiers — can evaluate each step in the reasoning chain
- Provides richer training signal for improving the model

#### Challenge: Data Collection
- Scoring intermediate steps is difficult to automate, even for verifiable tasks
- Human review of each step is expensive and doesn't scale
- A DeepMind paper proposes automated solutions (e.g., Monte Carlo rollouts to estimate step-level correctness)

#### Dual Use of PRM
1. **Training**: Use PRM scores to fine-tune the LLM for better reasoning
2. **Inference-time search guidance**: Use PRM during tree search/generation to score intermediate directions, prune bad paths, and continue promising ones — enables efficient search at inference time

---

## 4. Self-Correction

### The Problem
- Even trained reasoning models can make mistakes in their final answers
- Goal: develop methods for the LLM to detect and fix its own errors

### What Is Self-Correction?
- The model generates an initial output, evaluates/critiques it, revises it, and potentially repeats
- Process: Output 0 → Evaluate → Output 1 → Evaluate → Output 2 → ... → Final Answer

### Two Dimensions of Self-Correction

#### By Compute Type
1. **Inference-time**: Use more tokens/compute at generation time for revision (no retraining)
2. **Training-time**: Train the model specifically to be good at self-revision

#### By Feedback Source
1. **Intrinsic**: No external feedback — the model evaluates and revises using only its own judgment
2. **Extrinsic**: Access to external signals — reward models (PRM/ORM), tool outputs (code execution, error logs, API responses), or other feedback

### Training Self-Correction

#### SFT Approach
- Create training data with incorrect outputs followed by corrections; fine-tune on this data
- Research shows SFT alone is not significantly better than baseline for self-correction

#### Reinforcement Learning Approach
- Use RL with carefully designed reward terms to train the model for self-correction
- More effective than SFT (Supervised Fine-Tuning) — the model learns to detect and fix errors through the RL process
- The trained model performs better at inference-time revision because self-correction is internalized

### External Feedback in Practice
- Companies often have PRM/ORM models to score outputs
- Function-calling models can use tools (code interpreter, APIs) and receive execution feedback
- Error logs, bug reports, and tool outputs serve as external feedback for revision cycles
- Extrinsic self-correction is generally more practical and effective than intrinsic

---

## 5. Internalizing Search

### The Problem with Linear Reasoning
- Simple problems can be solved with a straightforward chain of thought
- Complex problems require trying different approaches, backtracking, and exploring multiple solution paths
- A single linear chain of thought is insufficient for complex problems

### Meta Chain-of-Thought (Meta-CoT)

#### System 1 vs System 2 Thinking
- **System 1 (simple)**: A single sequence of thoughts → final answer
- **System 2 (complex)**: Multiple reasoning attempts, backtracking, and exploration before reaching the correct answer

#### The Meta-CoT Approach
- Training data format: Question → z1 (attempt 1, possibly wrong) → z2 (attempt 2) → ... → zk (correct chain of thought → final answer)
- z1 through zk-1 are "latent thoughts" — the process of exploring and possibly failing
- For complex problems: more latent thoughts in training data
- For simple problems: fewer latent thoughts
- Data preparation is the most difficult part; can use LLMs to generate data with multiple reasoning attempts

#### What the Model Learns
- How to think, try different methods, backtrack, and continue until reaching the final solution
- **Adaptive thinking depth**: The model learns when to think more (complex questions) vs. when to think less (simple questions)
- At inference time, simple questions get quick answers; complex questions trigger extensive search and exploration

### Backtracking Patterns in Real Models
- The Meta-CoT paper analyzes models like o1, DeepSeek R1, and Gemini 2 thinking model
- Identified backtracking patterns: model generates a solution attempt → says "But wait..." or "Actually..." → backtracks → tries a different approach
- Pattern: search → backtrack → search → backtrack → search again
- These patterns emerge from training on data that includes search and backtracking examples

### Combining All Techniques: What Happens in o3
- The initial "thinking" phase (no visible tokens) is the model running search at inference time
- Verifiers (PRM) guide which directions to explore
- After the search phase, the model produces its visible chain-of-thought output with latent thoughts and reasoning traces
- Example: o3 took 3 minutes 30 seconds of thinking for a complex math question — extensive search and latent thought exploration before producing the final output

---

## 6. Deep Research: Practical Application

### What Is Deep Research?
- A practical application combining reasoning models with tools and multi-agent architectures
- Uses a reasoning/thinking model as the agent's core instead of relying on prompt engineering (e.g., ReAct)
- The model inherently knows how to think and reason — no explicit CoT prompting needed

### Architecture
- **Multi-agent system** (not a single multi-step agent)
- Multiple sub-agents, each with access to tools (web search, browser)
- Sub-agents perform independent research tasks
- A manager agent coordinates, summarizes collected information, compiles the final report, and shares it with the user

### OpenAI's Deep Research Feature
- First introduced around February; major update July 17 added visual browser access
- Visual browser enables the system to navigate, search, and extract information from web pages visually
- Research process takes tens of minutes; shows real-time activity and sources
- May ask clarifying questions before starting
- Produces comprehensive, detailed reports

### Connection to Course Project
- Project 4: Build a "deep research light" system
- Demonstrates practical application of reasoning models combined with agent architectures and tool use

---

## Key Takeaways

1. **Reasoning models** are LLMs that generate intermediate thinking traces before producing final answers — they are currently the most capable models available
2. **Inference-time scaling** (CoT, self-consistency, tree of thoughts, sequential revision) improves output quality by spending more compute at generation time without retraining
3. **Training-time approaches** (CoT fine-tuning, ORM, PRM, RL) embed reasoning capability directly into the model
4. **PRM is more powerful than ORM** because it scores individual reasoning steps, not just the final answer — and it can be used both for training and as an inference-time search guide
5. **Self-correction** can be achieved through inference-time prompting tricks or training with RL; extrinsic feedback (tools, reward models) is more effective than intrinsic self-evaluation
6. **Internalizing search** (Meta-CoT) trains models to explore, backtrack, and try multiple approaches — with adaptive thinking depth based on problem complexity
7. **Deep research** is a practical multi-agent application that combines reasoning models with web search and browsing tools to produce comprehensive research reports
8. All these techniques can be **combined** — modern reasoning models like o3 likely use inference-time search, PRM verification, internalized backtracking, and self-correction together
