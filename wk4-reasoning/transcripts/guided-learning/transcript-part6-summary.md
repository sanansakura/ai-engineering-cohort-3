# Week 4 Guided Learning - Part 6 Summary

## Self-Correction (Continued)

### Inference-Time Self-Correction

#### Intrinsic Self-Correction (Inference)
- The model is not trained for revision — only using prompt engineering tricks to make it revise
- No access to external feedback or reward models
- The model generates a response, then is asked to evaluate and improve it
- We don't really know which of the generated revisions (output 1, 2, or 3) is better without external signals

#### Extrinsic Self-Correction (Inference)
- Very similar to intrinsic, but with one key difference
- Has access to external feedback signals: reward models, tool outputs (e.g., code execution results, error logs), or API responses
- External feedback helps the model know whether its output is correct and what to fix
- More effective because the model gets concrete signals about errors

### Training-Time Self-Correction

#### The Goal
- Train the model to be inherently good at self-correction, not just rely on inference-time tricks
- The model should learn to detect mistakes and revise them as part of its generation process

#### SFT (Supervised Fine-Tuning) for Self-Correction
- One approach: create training data with incorrect outputs followed by corrections, then fine-tune
- Research shows SFT alone for self-correction is not significantly better than baseline
- Simply showing the model examples of corrections is not enough

#### Reinforcement Learning for Self-Correction
- A paper proposes using reinforcement learning with carefully designed reward terms
- The RL approach trains the model to self-correct without needing to know if its approach works in advance
- More effective than SFT for teaching self-correction
- The model learns to revise itself through the RL training process

#### Training-Time + Inference-Time Combined
- A model trained for self-correction (via RL) performs better at inference-time revision too
- When the trained model encounters incorrect output, it's generally better at identifying and fixing errors because that's what it was trained to do
- The training and inference approaches complement each other

### External Feedback in Practice
- Companies often have access to PRM/ORM reward models to score thoughts/outputs
- Models with function calling can use tools (code interpreter, APIs) and get execution feedback
- Error logs, bug reports, and tool outputs can all serve as external feedback for the next revision cycle
- Extrinsic self-correction is generally more practical and effective than intrinsic

## Internalizing Search

### The Fifth Approach: Internalizing Search into the Model

#### Simple vs Complex Problems
- Simple problems: can be solved with a straightforward chain of thought — write the solution from beginning to end
- Complex problems: may require trying different approaches, backtracking, and exploring multiple solution paths
- For complex problems, a single linear chain of thought is insufficient
