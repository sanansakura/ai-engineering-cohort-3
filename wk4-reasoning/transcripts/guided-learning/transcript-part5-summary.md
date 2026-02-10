# Week 4 Guided Learning - Part 5 Summary

## Process Reward Modeling (PRM)

### Motivation: Limitations of ORM
- ORM only scores the final answer, ignoring intermediate reasoning steps
- This means incorrect intermediate steps go undetected as long as the final answer happens to be correct
- PRM addresses this by scoring each intermediate step individually

### How PRM Works
- Training data: same format as ORM — question, sequence of intermediate thoughts, final answer
- Key difference: the label/score is assigned to each intermediate step, not just the final answer
- Each reasoning step gets its own correctness score
- PRMs have better visibility into the reasoning process — they can evaluate each step in the chain

### Advantages of PRM over ORM
- More capable and more useful as verifiers
- Better overview of each step in the reasoning chain
- Can identify where reasoning goes wrong, not just whether the final answer is correct
- More granular feedback for training

### Challenge: Scaling PRM Data Collection
- Scoring intermediate steps cannot easily be automated, even for verifiable tasks (like math)
- Humans need to review and score each intermediate step — this is expensive and doesn't scale
- A DeepMind paper proposes solutions to automatically scale PRM data collection
- The paper uses automated methods (e.g., Monte Carlo rollouts) to estimate step-level correctness

### Scoring Format
- Correct steps get positive scores (e.g., happy face / checkmark)
- Incorrect or unhelpful steps get negative scores (e.g., sad face / X)
- Neutral steps may be scored differently

### Summary of Training Approach 2 (ORM + PRM)
- Start from an LLM, generate CoT data
- Train an ORM or PRM reward model to score outputs
- Use the reward model to continue training/fine-tuning the LLM for better reasoning
- PRM provides more detailed feedback by scoring individual steps

### Dual Use of PRM
- **Use Case 1: Training** — Use PRM scores to continue training/fine-tuning the LLM to improve its reasoning capability
- **Use Case 2: Inference-time search guidance** — Use PRM at inference time to guide tree search / generation
  - During tree-of-thoughts or search-based generation, pass intermediate thought sequences to the PRM
  - PRM scores each direction — prune bad directions, continue promising ones
  - Enables efficient search by stopping exploration of low-scoring paths early
  - Example: at any point during generation, pass the sequence of thoughts to PRM; if score is low, stop exploring that direction

## Self-Correction

### The Problem
- Standard LLMs (without reasoning training) fail on many complex tasks (math, etc.)
- Even trained reasoning models can still make mistakes in their final answers
- Goal: develop methods where the LLM can detect and fix its own errors

### What Is Self-Correction?
- The LLM detects and revises its own response to arrive at a better final answer
- Process: Generate initial output → evaluate/critique it → revise it → potentially repeat
- Produces iteratively improved outputs (output 0 → output 1 → output 2 → final answer)

### Two Dimensions of Self-Correction

#### By Compute Type
1. **Inference-time self-correction**: Spend more tokens/compute at inference time for revision
2. **Training-time self-correction**: Train the model specifically to be good at revising

#### By Feedback Source
1. **Intrinsic self-correction**: No access to external feedback or reward models; the model must evaluate and revise using only its own judgment
2. **Extrinsic self-correction**: Has access to external feedback — reward models (PRM/ORM), tool outputs (code interpreter logs, API results), or other external signals
