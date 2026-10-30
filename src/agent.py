from langchain.agents import create_agent
from src.lib.model_init import model_init
from src.tools import get_claude_usage
from langchain.messages import HumanMessage
import asyncio

model = model_init("gpt-4o")

suggestion_agent = create_agent(
    model=model,
    tools=[get_claude_usage],
    system_prompt="""
You are an AI coding assistant usage agent. You can collect the usage data of various AI coding assistants and provide helpful advice on how to optimize the user's token usage.
You can access the data of the following AI coding assistants:

* Claude (including Claude Code)

If asked about an AI coding assistant not in the list respond with:
<unrecognized_assistant>Sorry. I cannot advise you on that coding assistant.</unrecognized_assistant>
Do not include the XML tags in the response in this case.

When giving suggestions make sure they are relevant to the data, not only general advice on optimizing LLM usage. Give your reasoning for your suggestion that references the actual data you have.
""")

messages = []

def send_message(content: str):
    messages.append(HumanMessage(content))
    messages.append(suggestion_agent.invoke(
        {"messages": messages}
    )["messages"][-1])
    return messages