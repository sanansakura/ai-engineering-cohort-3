# Week 4 Guided Learning - Part 8 Summary

## Deep Research

### Introduction to Deep Research
- Deep research is a practical application that combines reasoning models with tools
- Builds on multi-agent systems and multi-step agent architectures covered in previous weeks

### How Deep Research Works

#### Architecture
- Uses a reasoning/thinking model instead of a traditional LLM as the agent's core
- The agent communicates with tools (web search, browser, etc.)
- Unlike previous agent setups that relied on prompt engineering (e.g., ReAct prompting), deep research agents use models that inherently know how to think and reason
- The model itself handles the reasoning — no need for explicit CoT prompting

#### OpenAI's Deep Research Feature
- Introduced by OpenAI around February (first announced)
- July 17 update: Deep research gained access to a visual browser as part of its capabilities
- This makes it even more capable — it can visually browse, search, and extract information from the web
- The feature is accessible through OpenAI's ChatGPT UI

#### How It Works in Practice
- Select the deep research preset in ChatGPT
- Ask a question (e.g., "Create a detailed summary of every technique for training, thinking, and reasoning models")
- The system may ask clarifying background questions before starting
- Takes a very long time — typically tens of minutes to complete
- Shows activity and sources being consulted during the research process
- Produces a detailed, comprehensive report

### Deep Research Architecture: Multi-Agent System
- Deep research is not a single multi-step agent — it's a multi-agent system
- Multiple sub-agents work together:
  - Each sub-agent has access to tools (search, browsing)
  - Sub-agents perform independent research tasks on the web
  - A manager agent coordinates the sub-agents
- Once all sub-agents complete their work, the manager agent:
  - Summarizes the collected information
  - Compiles the final report
  - Shares the report with the user

### Connection to Course Project
- Project 4 involves building a "deep research light" system
- Students will see many examples of using different reasoning capabilities in the project
- Demonstrates practical application of reasoning models combined with agent architectures and tool use
