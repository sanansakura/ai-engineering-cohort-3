# Office Hours Transcript Part 1 Summary

## React Pattern and Reasoning LLMs

### What is React?
- React is a **prompting technique** only—not training or fine-tuning
- Uses a system prompt with **think → act → observe** cycle
- Includes few-shot examples in the system prompt
- Frameworks (e.g., LangChain) implement this under the hood—no manual prompt creation needed
- Reasoning LLMs make the cycle more powerful because they are trained to reason

### How React Works
- LLM receives system prompt + user query, produces tokens following the loop
- When action needed: produces parseable format → agent runtime parses → executes tool → appends observation → sends back to LLM

## Tool Calling

### Parameter Mapping
- LLM relies on internal understanding of words, concepts, arguments
- With good function name + description + inputs, LLM maps arguments to parameters
- Bigger models (1B → 3B → 7B) handle tool calling much better
- Smaller models may fail on multiple simultaneous tool calls; larger models handle this

### Tool Introduction Paradigms
- **Manual**: Introduce tools via schema to any LLM; works if model is big enough
- **Trajectory training**: Train on tool-calling examples (OpenAI pioneered); Palama, Qwen K2.5, etc. use this

### Built-in Tools
- GPT models: trained on fundamental tools (web search, terminal, bash)
- **Composer** (Cursor): coding LLM fine-tuned on ~10+ tools (read/edit files, run commands)
- Custom tools: use MCP or other methods to introduce

## Agent Types (create_react_agent, create_tool_calling_agent, create_agent)
- All are essentially the same; agents assume tools + cycle
- React = cycle part; tools = tools part; together = agent
- Tools are a key component—agent without tools doesn’t make sense

## Workflows vs. Agents

### Workflows
- **Static** graph; developer defines steps ahead of time
- Fixed sequence; no loop; LLM has no autonomy
- Multiple LLM calls possible but predetermined

### Agents
- **Dynamic**; agent figures out next step
- Full autonomy: think → break task / call tools / produce final answer
- Agent decides when to continue vs. finish

## LLM vs. Agent Runtime

### Agent (Runtime)
- Pure software; no ML, no parameters
- Orchestrates: LLM, tools, memory, user I/O
- Does not think or produce tokens
- Parses tool calls from LLM output, executes tools, appends results to context

### LLM
- The “brain”; thinks, produces tokens, decides when to use tools
- Just a mathematical model (matrices); cannot call tools by itself
- Agent runtime is needed to bridge LLM output to tool execution

## MCP and Tool Awareness
- Agent loads available tools (including from MCP servers)
- Sends tool list to LLM as part of context
- LLM must know about tools to produce tool-calling tokens

## MCP vs. Plugins
- Instructor will research plugins; MCP covered in guided learning
- MCP: standardize tool exposure; reuse existing MCP servers; update config to add tools

## AI Agent vs. Agentic AI Systems
- **AI agent**: wrapper around LLM + tools + loop (software you implement)
- **Agentic system**: broader system that includes agents and other components
