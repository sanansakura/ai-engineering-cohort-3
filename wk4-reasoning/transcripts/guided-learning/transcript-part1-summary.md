# Week 4 Guided Learning - Part 1 Summary

## Introduction to Thinking and Reasoning Models

### What Are Reasoning Models?
- Week 4 focuses on thinking and reasoning models — the most capable models currently available
- Reasoning models are still LLMs, but they are trained/capable of generating intermediate reasoning traces before producing a final answer
- Reasoning traces are typically multi-step and can involve multi-path exploration (the model may explore different reasoning directions)
- Once reasoning/thinking is over, the model produces its final response

### Two Main Strategies to Build Reasoning Models
- **Inference-time scaling**: Techniques applied at generation time without retraining
- **Training models with reasoning capability**: Training/fine-tuning models to internalize reasoning

### Topics Covered This Week
- Outcome reward modeling and process reward modeling + reinforcement learning
- Approaches to internalize search into the model
- Deep research as an example of combining reasoning models and tools
- Project 4: Building a deep research light system

## Live Demos: Reasoning vs Non-Reasoning Models

### OpenAI Model Naming Conventions
- Models starting with "o" (o3, o3 pro, o4 mini) are reasoning models
- Models starting with numbers (GPT-4o, GPT-4.5, GPT-4.1) are not reasoning models
- Non-reasoning models may still show some reasoning behavior but are not specialized/trained for it
- o4 mini is described as a more efficient version for reasoning — "fastest at advanced reasoning"

### Demo: Counting from 1 to 10
- **GPT-4o (non-reasoning)**: Immediately started answering with no thinking pause; gave an incorrect time estimate (said ~10 seconds); very fast but inaccurate
- **o4 mini (reasoning)**: Paused for ~9 seconds to think before responding; showed "thinking" indicator; produced a more accurate and considered answer
- **o3 (more capable reasoning)**: Took even longer to think (~1+ minute); generated more reasoning tokens; more expensive but more thorough

### Key Observations
- Reasoning models think first, then present the final result
- OpenAI does not show the actual reasoning traces — the displayed "thoughts" are reworded/summarized, not the raw tokens
- More capable reasoning models (o3 vs o4 mini) take longer but may produce better results
- For day-to-day tasks, o4 mini is sufficient; for complex tasks, o3 is recommended; o3 pro for very complex/reliable needs

### Other Reasoning Models and Leaderboards
- Anthropic has Claude Opus 4 as a high-degree reasoning model
- LM Arena leaderboard ranks all models — many top models are reasoning models
- Kimi K2 by Moonshot (Chinese company) ranked #5 despite being from a smaller company; notably a non-thinking model — very impressive
  - Uses a modified MIT license
- Alibaba's QWen models also competitive
- GPT-4.5 (non-reasoning) and Claude Sonnet 4 also rank highly despite not being reasoning models

### Open-Source Reasoning Models via Hyperbolic
- Demonstrated using reasoning models through Hyperbolic API
- Increased max tokens to 10,000 because reasoning models generate many tokens during thinking
- Some platforms (like Hyperbolic) show the actual reasoning traces (the exact tokens generated during thinking), unlike OpenAI's summarized version
