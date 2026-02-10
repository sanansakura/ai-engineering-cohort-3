# Week 4 Guided Learning - Part 7 Summary

## Internalizing Search (Continued)

### Meta Chain-of-Thought (Meta-CoT) Paper

#### System 1 vs System 2 Thinking
- The paper discusses "system two" thinking — complex questions requiring more attention and trying different methods
- **Simple questions (System 1)**: Answer can be a straightforward sequence of thoughts followed by the final answer
- **Complex questions (System 2)**: Answer is not just a linear sequence of thoughts — it may involve branching, backtracking, and exploring multiple paths

#### The Meta-CoT Approach
- Instead of training on data with a single chain of thought per question, collect data with a **sequence of chains of thought** (z1, z2, ... zk)
- Each zi is a "latent thought" — a complete reasoning attempt that may or may not be correct
- The final chain of thought (zk) contains the correct solution with its own intermediate steps followed by the final answer
- z1 through zk-1 are latent thoughts representing the process of thinking, exploring, and possibly failing before reaching the right approach

#### Training Data Format
- Question → z1 (possibly incorrect attempt) → z2 (another attempt) → ... → zk (correct chain of thought with final answer)
- For complex problems: more latent thoughts in the training data
- For simple problems: fewer latent thoughts
- If trained on such data, the model learns to think, try different methods, backtrack, and continue until it reaches the final solution

#### Data Preparation
- The most difficult/important part is data preparation
- Can use LLMs to generate such data — producing multiple reasoning attempts for each question
- The data should include examples of backtracking and strategy changes

### Demo: Backtracking in Real Models

#### ChatGPT o3 Thinking Process
- Asked o3: "What are the most difficult questions in the International Mathematical Olympiad and why?"
- The model's thinking process showed: "The user wants to know the hardest problem. I'm going to search..."
- The model searched, collected information, and may change strategy or backtrack during thinking

#### Analyzing Backtracking Patterns in Existing Models
- The Meta-CoT paper analyzes existing reasoning models (o1, DeepSeek R1, Gemini 2 thinking model)
- They identify specific backtracking patterns in model outputs:
  - Model generates a solution attempt
  - At some point says something like "But wait..." or "Actually, since this is..."
  - Model backtracks to a previous point and tries a different approach
  - This pattern is observed in o4/o1 and DeepSeek R1

#### Visual Examples
- The paper includes visualizations showing how models search and backtrack
- Pattern: search → backtrack → search → backtrack → search again
- Models trained with this data show clear search and backtracking behavior

### Key Observation: Adaptive Thinking Depth
- Because training data has fewer latent thoughts for simple questions and more for complex ones, the model learns to adapt
- At inference time:
  - **Simple questions**: Model quickly arrives at the answer without extensive search
  - **Complex questions**: Model performs more extensive search, tries multiple approaches, backtracks more
- The model implicitly learns when to think more vs. when to think less

### Combining All Techniques

#### What Happens Behind the Scenes in Models Like o3
- The initial "thinking" phase (where no tokens are shown) is likely the model running search at inference time
- The model uses verifiers (PRM) to determine which directions are promising
- After the search phase, the model produces its visible chain-of-thought output
- The final CoT output includes latent thoughts and reasoning traces
- Example: o3 took 3 minutes and 30 seconds of thinking, involving lots of searches and latent thought exploration, before producing the final visible output
