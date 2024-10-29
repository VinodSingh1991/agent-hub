from src.sales_assistant.agent import Assistant, State
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver
from src.public_util.error_handling import create_tool_node_with_fallback
from src.sales_assistant.prompt import syatem_prompt
from src.llm_factory.acidaes_llm import next_llm
from src.sales_assistant.tools import tools_next
import uuid


# Configuring and running the application
def run_application(user_input):
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id,  "recursion_limit": 10}}

    # Get the LLM
    model = next_llm.get_open_ai_llm_with_tools(tools_next)

    # Create the Assistant with tools and graph
    assistant_runnable = syatem_prompt | model 
    assistant = Assistant(assistant_runnable)

    state_graph = StateGraph(State)
    state_graph.add_node("assistant", assistant)
    state_graph.add_node("tools", create_tool_node_with_fallback(tools_next))
    state_graph.add_edge(START, "assistant")
    state_graph.add_conditional_edges("assistant", tools_condition)
    state_graph.add_edge("tools", "assistant")

    # Initialize memory
    memory = MemorySaver()
    app = state_graph.compile(checkpointer=memory)

    # Process user input
    return app.invoke({"messages": [("user", user_input)]}, config=config)

def start_sales_app(msg):

    messages = run_application(msg)
    message = messages.get("messages")
    
    if message and isinstance(message, list):
        message = message[-1]

    return message

