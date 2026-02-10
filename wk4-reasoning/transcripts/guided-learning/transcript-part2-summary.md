# Week 4 Guided Learning - Part 2 Summary

## Inference-Time Scaling: Building Reasoning Without Retraining

### Two Buckets for Building Reasoning Models
- **Inference-time scaling**: Spend more compute at generation time without changing model parameters — the model becomes more capable at inference
- **Training-time scaling**: Continue training the LLM so it develops reasoning capability internally
- Focus of this section: inference-time approaches

### Approach 1: Chain-of-Thought (CoT) Prompting

#### Without CoT
- If you ask a model a complex question (e.g., math), it may jump to a final answer without intermediate reasoning
- The LLM is not expected to produce multi-step reasoning on its own

#### Few-Shot CoT Prompting
- Add examples in the prompt context showing how to reason step-by-step for a similar question
- Example: "Two boxes with three balls each. How many? 2 x 3 = 6. Answer: 6."
- Then ask the actual question — the model follows the demonstrated reasoning pattern
- Providing multiple examples (few-shot) further guides the model

#### Zero-Shot CoT Prompting
- Based on the "Large Language Models are Zero-Shot Reasoners" paper
- Simply add "Let's think step by step" to the prompt
- No examples needed — the model has learned from training data that includes step-by-step reasoning
- Works because models have seen many examples with reasoning traces in their training data

#### Demo: CoT with LLaMA 3
- Without CoT: LLaMA 3 failed the math question (said "three red bags with apples" — wrong)
- With few-shot CoT example: The model performed better, doing calculations and arriving at the correct answer (29 items total)
- Shows how prompting can push non-reasoning models to reason

#### Visualization of CoT
- Input → Thought 1, Thought 2, ... Thought N → Final Answer
- Each thought is an intermediate reasoning step (e.g., "2 x 7 = 14")
- In practice, each thought may have a text description followed by computation

### Approach 2: Self-Consistency (Parallel Sampling)

#### Core Idea
- Instead of spending compute on a single reasoning chain, generate multiple complete responses (N parallel generations) and pick the best one
- Also known as "parallel sampling" or "best-of-N sampling" in different frameworks
- Full control over compute budget — more samples = more tokens generated = better overall response

#### Combining CoT with Self-Consistency
- Each of the N parallel branches uses chain-of-thought reasoning
- After all branches generate their own reasoning chain and final answer, pick the best response
- Evaluation shows self-consistency (blue) outperforms single-generation CoT (red) across multiple domains and benchmarks

### Picking the Best Response

#### Method 1: Majority Voting
- Compare the N final answers and pick the one that the majority agree on
- Example: 4 generations produce answers, majority says "29" → pick "29"
- Works well for tasks with verifiable correct answers (math, factual questions)

#### Method 2: Reward Model Scoring
- For subjective tasks (writing, open-ended questions), majority voting doesn't work since all answers may be different but valid
- Use a reward model trained on pairs of prompts and responses with human-scored quality ratings
- The reward model assigns a quality score to each generation; pick the highest-scored response
- Enables self-consistency to work across diverse domains (writing, coding, etc.) — as long as the reward model is trained on similar data
