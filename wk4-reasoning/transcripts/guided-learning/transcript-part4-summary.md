# Week 4 Guided Learning - Part 4 Summary

## Training-Time Approaches for Reasoning

### Transition from Inference-Time to Training-Time Scaling
- Previous techniques were all at inference time — no model parameters were changed
- Now focusing on training the model itself to develop reasoning capability
- These approaches spend more time/compute on training so the model internalizes reasoning

### Approach 1: Training with Chain-of-Thought Data (Fine-Tuning on CoT)

#### Generating CoT Training Data
- Start with an LLM that is not initially capable of generating chain-of-thought reasoning
- Use CoT prompting (from inference-time techniques) to get the model to produce reasoning traces
- Generate multiple outputs using parallel sampling; identify the best answers (e.g., for math — check if the final answer is correct)
- If the final answer is correct, we now have a rationale (the intermediate reasoning steps) paired with the question
- This question + rationale pair forms one training example

#### Iterative Fine-Tuning Process
- Collect a batch of these CoT examples as training data
- Fine-tune the model on this data
- The improved model can then generate even better CoT data for the next round of training
- Iteratively repeat: the model keeps getting better at generating intermediate reasoning steps

#### Special Tokens for Thinking
- To distinguish between thinking/reasoning tokens and final answer tokens, define special tokens
- Example: `<think>` and `</think>` tags to wrap the reasoning process
- Training data format: Question → `<think>` reasoning steps `</think>` → Final Answer
- After fine-tuning, the LLM learns to generate `<think>` tokens, reason within them, then produce the final answer

#### Demo: Tokenizer for Reasoning Models
- Showed how special tokens work in practice using a tokenizer
- `<think>` becomes a single token (e.g., token ID 128798)
- `</think>` becomes another single token (e.g., token ID 128799)
- These two special tokens are used to delineate the reasoning process in the model's output

#### Key Insight
- Even models not advertised as "reasoning models" (e.g., GPT-4) have been trained on datasets containing chain-of-thought intermediate steps
- These models learn to generate some reasoning traces naturally because their training data includes many examples with step-by-step solutions
- This is the first training approach: fine-tune on CoT data to make the model reason

### Approach 2: Outcome Reward Modeling (ORM)

#### Connection to Inference-Time Techniques
- At inference time, parallel sampling generates multiple outputs and picks the best one (e.g., via reward model)
- The training equivalent: continue fine-tuning the model based on scored/ranked outputs
- Generate multiple responses, score them, and use the best ones for continued training

#### How ORM Works
- Training data format: prompt + sequence of intermediate reasoning steps + final answer + label (score)
- The label/score indicates how accurate/good the final answer is
- For verifiable tasks (math, coding), the score can be automatically determined by checking the final answer
- Train a reward model to predict this score given a prompt and response
- The reward model is essentially a copy of the LLM with an added scoring head

#### Limitation of ORM
- ORM only looks at the final answer to assign a score
- It does not examine or score intermediate reasoning steps
- Even if there are incorrect or important intermediate thoughts, ORM ignores them
- The model may learn some implicit correlations between intermediate steps and final answer quality, but this is indirect
- This limitation motivates the next approach: Process Reward Modeling (PRM)
