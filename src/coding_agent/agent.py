import functools
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import Literal
from src.llm_factory.acidaes_llm import next_llm
from langgraph.prebuilt import create_react_agent
from src.coding_agent.tools import tavily_tool,python_repl
from src.coding_agent.utilities import agent_node

members = ["Researcher", "Coder"]

system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers:  {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)
options = ["FINISH"] + members


class RouteRespose(BaseModel):
    next: Literal[tuple(options)]  # type: ignore


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Given the conversation above, who should act next?"
            " Or should we FINISH? Select one of: {options}",
        ),
    ]
).partial(options=str(options), members=", ".join(members))

llm = next_llm.get_open_ai_llm()

def superviser_agent(state):
    supervisor_chain = prompt | llm.with_structured_output(RouteRespose)
    return supervisor_chain.invoke(state)

research_agent = create_react_agent(llm, tools=[tavily_tool])
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")

code_agent = create_react_agent(llm, tools=[python_repl])
code_node = functools.partial(agent_node, agent=code_agent, name="Coder")