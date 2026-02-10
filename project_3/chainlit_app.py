# ---------------------------------------------------------
# Chainlit Web Search Agent

import chainlit as cl
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage

from ddgs import DDGS


# ---------------------------------------------------------
# Define the web search tool
# ---------------------------------------------------------

@tool
def web_search(query: str) -> str:
    """Search the web for information using DuckDuckGo. Returns titles and URLs of top results."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
    if not results:
        return "No results found."
    return "\n".join(f"- {r['title']}: {r['href']}" for r in results)


@tool
def calculate(expression: str) -> str:
    """Evaluate a simple math expression. Use for arithmetic like '5*5', '10+3', '20/4'. Only safe expressions with numbers and +-*/()."""
    import re
    if not re.match(r"^[\d\s\+\-\*\/\(\)\.]+$", expression):
        return "Invalid expression - only numbers and + - * / ( ) allowed."
    try:
        return str(eval(expression))
    except Exception:
        return "Could not evaluate that expression."


# ---------------------------------------------------------
# Create the agent (once at startup)
# ---------------------------------------------------------

llm = ChatOllama(model="llama3.2:3b")
system_prompt = """You are a helpful assistant with two tools: calculate for math (e.g. "5*5" or "10+3"), and web_search for current info. For arithmetic, use the calculate tool. For facts you need to look up, use web_search. Always give a clear final answer to the user."""
agent = create_react_agent(llm, [calculate, web_search], prompt=system_prompt)


def _get_final_content(messages):
    """Extract the final human-readable answer from the assistant, skipping tool-call JSON."""
    for msg in reversed(messages):
        if not isinstance(msg, AIMessage):
            continue
        if hasattr(msg, "content") and msg.content:
            content = str(msg.content).strip()
            if not content:
                continue
            # Skip content that looks like raw tool-call schema
            if content.startswith("{") and '"name"' in content and '"parameters"' in content:
                continue
            return content
    return "I couldn't generate a response. Please try rephrasing your question."


# ---------------------------------------------------------
# Chainlit message handler
# ---------------------------------------------------------
@cl.on_message
async def handle_message(message: cl.Message):
    """Handle user messages and stream agent responses."""
    response = await agent.ainvoke({
        "messages": [HumanMessage(content=message.content)]
    })
    content = _get_final_content(response["messages"])
    await cl.Message(content=content).send()


# ---------------------------------------------------------
# Welcome message
# ---------------------------------------------------------
@cl.on_chat_start
async def start():
    await cl.Message(
        content="Hello! I'm your web search agent. Ask me anything and I'll search the web to find answers."
    ).send()
