import sqlite3
import os
from typing import Annotated
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode
from llm_factory.llm_getter import get_acidaes_llama_llm_with_tools
from langgraph.graph.message import AnyMessage, add_messages
from langchain.prompts import ChatPromptTemplate
from typing_extensions import TypedDict
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from po_assistant.custom_tools.search_tools import SearchTools

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable
        
    def __call__(self, state: State):
        while True:
            # configuration = config.get("configurable", {})
            # passenger_id = configuration.get("passenger_id", None)
            # state = {**state, "user_info": passenger_id}
            result = self.runnable.invoke(state)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}


# Define Tools for LangGraph
search = SearchTools().search_internet
tools = [search]
model = get_acidaes_llama_llm_with_tools(tools)

def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }

def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )
# User input to test the agent
#user_input = input("Enter your question about leads: ")

user_prompt = ChatPromptTemplate.from_messages(
     [
        ("system", 
        "Uncover groundbreaking research in the field of {messages}"
        "Think like you are a Senior Researcher and expert in the Oxford University Research Institute. you have been working in the field of ground breaking research for over 10 years and has published numerous papers in top-tier conferences and journals. He is passionate about pushing the boundaries of research and is always on the lookout for new and exciting projects to work on. you explore and share your latest innovations in the field of {messages}"
        "Create a most amazing and write into the well and standered formate on the {messages}"
        "please make sure you have a good understanding of the topic and have done your research before you start writing. you can use the internet to find information on the topic and use it"
        "Note: you can use the internet to find information on the topic and use it and write detail information on the {messages}"
        "write minimum 1000 words on the {messages}"
        ),
        ("placeholder", "{messages}")
    ]
)

assistant_runnable = user_prompt | model

#print("assistant_runnable", assistant_runnable)


builder = StateGraph(State)

builder.add_node("assistant", Assistant(assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

memory = MemorySaver()

app = builder.compile(checkpointer=memory)

import uuid
thread_id = str(uuid.uuid4())

config = {
    "configurable": {
        # The passenger_id is used in our flight tools to
        # fetch the user's flight information\
        # Checkpoints are accessed by thread_id
        "thread_id": thread_id,
    }
}
         
def start_po_app(msg):
    # print("msg", msg)
    
    # return msg
    messages = app.invoke({"messages": [("user", msg.message)]}, config)
    message = messages.get("messages")
    if message:
        if isinstance(message, list):
                message = message[-1]
    
    return message