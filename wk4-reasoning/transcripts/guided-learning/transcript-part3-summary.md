# Week 4 Guided Learning - Part 3 Summary

## Inference-Time Scaling (Continued)

### Approach 3: Tree of Thoughts (ToT)

#### Text Generation as a Search Problem
- The text generation/decoding process can be viewed as a search problem
- We have an input and can control the output generation by exploring different intermediate paths

#### How Tree of Thoughts Works
- Generate several intermediate reasoning steps (thoughts) from a given point
- Score each intermediate step and pick the most promising ones to continue
- Expand the best paths further — e.g., generate 4 more thoughts from a high-scoring node
- Prune low-scoring branches and continue exploring high-potential branches dynamically
- The best path with the highest cumulative score forms the final output

#### ToT vs Self-Consistency
- Not fundamentally different from self-consistency, but more focused on efficiency
- Self-consistency generates many full parallel branches; ToT is smarter about which branches to expand
- ToT treats generation as a tree search, pruning bad directions early and investing compute in promising ones

#### Beyond ToT
- Many more approaches exist that treat text generation as a search problem
- A recommended paper evaluates different methods: parallel sampling, various search strategies, tree of thoughts, and more advanced search techniques
- Results show these methods can significantly improve accuracy in domains like math
- Beam search is one variant explored — expanding the top-k paths at each step

### Parallel vs Sequential Sampling

#### Parallel Sampling
- All approaches so far (self-consistency, ToT) spend compute budget in parallel
- Generate multiple branches/responses simultaneously

#### Sequential Revision (Approach 4)
- Instead of parallel exploration, sequentially extend computation
- The context passed to the LLM includes the original prompt + chain-of-thought + the model's response
- Ask the same (or different) model to revise/improve the response
- Repeat for a fixed number of iterations (k)
- Each iteration, the model sees its previous output and improves upon it

#### When to Use Which
- **Sequential sampling** is better for easier/medium difficulty questions — a single revision pass can fix simple mistakes
- **Parallel sampling** may be better for complex/difficult questions — trying fundamentally different approaches has a higher chance of finding the right direction
- For complex problems, sequential revision may get stuck in the same wrong direction, while parallel sampling explores diverse solution paths

### Summary of Inference-Time Scaling

#### Key Techniques Covered
1. **Chain-of-Thought prompting** — adding intermediate reasoning steps via prompting
2. **Self-consistency / parallel sampling** — generating multiple responses and picking the best
3. **Tree of Thoughts** — treating generation as a tree search, expanding promising branches
4. **Sequential revision** — iteratively improving a response over multiple passes
5. **Monte Carlo Tree Search (MCTS)** — mentioned as another approach (not covered in detail)

#### Core Principle
- All inference-time scaling techniques trade off more compute at inference time for better outputs
- The model parameters are not changed — only more tokens are generated
- These techniques can be combined (e.g., CoT + self-consistency, ToT + reward models)
- The fundamental idea: let the model think in different ways and different generated thoughts before committing to a final answer
