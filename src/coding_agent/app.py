import os
from langchain_core.messages import HumanMessage
from typing import Sequence, Annotated
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from src.coding_agent.agent import superviser_agent, code_node, research_node, members
import uuid
from langgraph.graph.message import AnyMessage, add_messages


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    next: str


def app_executer(user_input: str):

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id, "recursion_limit": 10}}

    workflow = StateGraph(State)
    workflow.add_node("Researcher", research_node)
    workflow.add_node("Coder", code_node)
    workflow.add_node("supervisor", superviser_agent)

    for member in members:
        # We want our workers to ALWAYS "report back" to the supervisor when done
        workflow.add_edge(member, "supervisor")

    conditional_map = {k: k for k in members}
    conditional_map["FINISH"] = END

    workflow.add_conditional_edges(
        "supervisor", lambda x: x.get("next"), conditional_map
    )
    workflow.add_edge(START, "supervisor")
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    initial_input = {"messages": [("user", user_input)]}
    return app.invoke(initial_input, config=config)


def run_coding_agent(msg):
    # Set up initial input with 'messages' as a list containing the user message dictionary

    # Invoke the app with the correctly formatted input
    messages = app_executer(msg)
    message = messages.get("messages")

    print("Message:", message)

    # Extract the last message if available
    if message and isinstance(message, list):
        message = message[-1]

    return message
