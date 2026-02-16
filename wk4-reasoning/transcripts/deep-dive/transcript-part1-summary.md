# Deep-Dive Part 1 Summary

## Context and roadmap

### Project 5 (brief)
- Project 5 released: multimodal agent (image/video generation) with a router (language vs image/video model).
- Recommendation: run on GPU (e.g. Google Colab); image/video models are expensive.

### Project 4 deep dive: deep research
- Deep research: thorough web study → long report (e.g. ChatGPT, Gemini).
- Project 4 builds a simpler version.
- Two ways to make models “think”: **inference-time scaling** (prompting, no weight change) vs **training** (SFT/RL to get reasoning).
- Roadmap: inference-time techniques (few-shot, zero-shot CoT, self-consistency, sequential revision, ToT) → inspect DeepSeek-R1 → build deep-research agent → optional multi-agent.

## Environment and setup

### Environment
- Conda or UV; kernel: `deep_research` (not deep_research V3).
- UV preferred for speed.

### Ollama
- Run `ollama serve` in a separate terminal.
- Models: `llama3.2:3b`, `deepseek-r1:1.5b`, `qwen2.5:3b-instruct` (pull if missing).

## Inference-time scaling: few-shot chain-of-thought

### GPT-2
- Completion model (no instruction tuning); good for showing effect of prompting.
- Hugging Face `pipeline("text-generation", model="gpt2")`; optional `torch.float16`, `device="mps"` (Mac).
- Without few-shot: sends question → poor/no step-by-step reasoning.
- Few-shot: add examples in format “Steps: … Therefore, the answer is X” → GPT-2 follows format (quality still limited).

### Llama 3.2
- Instruction-tuned; already does step-by-step reasoning.
- Few-shot used to **control format**: e.g. `[GIVEN]` / `[FIND]` / `[SOLVE]` / `[ANSWER]`.
- OpenAI client: `base_url="http://localhost:11434/v1"`, messages with `role` and `content`.

## Zero-shot chain-of-thought

- Single cue: append **“Let’s think step by step”** to the question (from “Large language models are zero-shot reasoners”).
- No examples; often improves answers; common in practice.
- Same client/model; just change the prompt.

## Self-consistency

### Idea
- **Best-of-N**: sample N times, pick best (e.g. majority vote on final answer).
- Often combined with CoT: CoT + multiple samples + majority voting.

### Implementation
- Prompt: “Answer with step-by-step reasoning” and **“End with: Therefore, the answer is &lt;number&gt;”** for parsing.
- `cot_answer(question, temperature)`: one completion; regex to extract “the answer is X”.
- Loop N times (e.g. 5), collect answers; `collections.Counter(answers).most_common(1)` for winner.
- Higher temperature → more diversity; good example when majority is correct but some runs wrong.

## Sequential revision

- **Sequential** (vs parallel in self-consistency): one draft → send draft + “evaluate and improve” → repeat.
- System prompt: “You are a helpful assistant, keep answers clear and correct.”
- Loop: get draft → new messages with original question + current draft + “Please revise, make clearer and more accurate” → replace draft; repeat for `max_steps`.
- More inference compute; can fix mistakes across rounds.

## Tree of thought (ToT)

### Concept
- Treat reasoning as **search**: expand partial solutions, score, prune (beam), keep top-K.
- More efficient than generating many full chains then voting.

### Word ladder (no LLM)
- Problem: transform word A → word B, one letter change per step, all in vocabulary.
- `neighbors(word, vocab)`: all words one character different and in vocab.
- `tree_of_thought(start, goal, vocab, max_depth, beam_width)`: frontier of paths; expand, sort by heuristic (e.g. edit distance to goal), keep top `beam_width`.
- Shows ToT as **algorithmic search**, not only LLM.

### LLM-based ToT
- **propose_thought(question, state, k)**: prompt LLM for k next steps from current partial solution (state).
- **score_state(question, state)**: prompt LLM to score 1–10 “how promising”; parse number; fallback 5.
- **tree_of_thought(question, depth, width)**: frontier = list of (state, score); for each step, expand each state with `propose_thought`, score new states, sort by score, keep top `width`; repeat until `depth`.
- Same idea as word ladder but “thoughts” from LLM and LLM as scorer; used in “pro” style systems (search over solution tree).
