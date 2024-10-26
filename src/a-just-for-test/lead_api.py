import sqlite3
import logging
import re

from typing import Annotated
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode
from src.llm_factory.acidaes_llm import next_llm
from langgraph.graph.message import AnyMessage, add_messages
from langchain.prompts import ChatPromptTemplate
from typing_extensions import TypedDict
from langgraph.prebuilt import ToolNode, tools_condition


# Initialize logging (this can be configured more globally)
logging.basicConfig(level=logging.INFO)


@tool
def validate_markdown(message: str):
    """
    Removes markdown-style code block delimiters (```) and the ```markdown``` pattern from a given string.

    Args:
        message (str): The input string that may contain triple backticks and markdown code blocks.

    Returns:
        str: The string with all markdown code block delimiters and ```markdown``` patterns removed.

    Notes:
        - The tool must return the output in markdown structure.
        - The output format should not be changed beyond removing the markdown-style delimiters.
    """

    if message:
        return re.sub(r"```markdown|```", "", message)

    return ""


@tool
def get_all_lead_details(userInput: str):
    """

    Description: Provide List of all Leads list
    all the list, detail list, top leads, follow-up information, and priority leads. lead list
    Fetch all lead details from the Leads table in the database.
    Fetch all Record in the table > tbody > tr > td > th formate

    Returns:
    provide the detail for the following columns: LeadID, FirstName, Amount, Email, Phone, CreatedBy
    dict: A dictionary containing all lead details fetched from the Leads table.
        The tool must return the output in the markdown structured.
         Tables should follow the format for: **table > tbody > tr > td > th**. ".
    """

    conn = None
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        logging.info("Connected to database")

        # Execute query to fetch all rows from Leads table
        query = "SELECT LeadID, FirstName, Amount, Email, Phone, CreatedBy FROM Leads"
        logging.info("Executing query: %s", query)
        cursor.execute(query)

        # Fetch all rows and extract column names
        rows = cursor.fetchall()
        print("rows", rows)
        column_names = [column[0] for column in cursor.description]
        # results = convert_response_to_modal("table", {"rows": rows, "columns": column_names})
        results = [dict(zip(column_names, row)) for row in rows]

        logging.info("Query executed successfully, fetched %d rows", len(rows))
        print("results", results)
        return results

    except sqlite3.Error as e:
        logging.error("SQLite error: %s", e)
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info("Database connection closed")


@tool
def get_all_actionable_leads(userInput: str):
    """

    Description: Provide List of actionable Leads list
    Fetch actionable lead details from the Leads table in the database.
    Fetch all lead details from the Leads table in the database.
    Fetch all Record in the table > tbody > tr > td > th formate

    Returns:
    provide the detail for the following columns: LeadID, FirstName, Amount, Email, Phone, CreatedBy
    dict: A dictionary containing all lead details fetched from the Leads table.
        The tool must return the output in the markdown structured.
         Tables should follow the format for: **table > tbody > tr > td > th**. ".
    """

    conn = None
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        logging.info("Connected to database")

        # Execute query to fetch all rows from Leads table
        query = "SELECT LeadID, FirstName, Amount, Email, Phone, CreatedBy FROM Leads where Amount > 200"
        logging.info("Executing query: %s", query)
        cursor.execute(query)

        # Fetch all rows and extract column names
        rows = cursor.fetchall()
        print("rows", rows)
        column_names = [column[0] for column in cursor.description]
        # results = convert_response_to_modal("table", {"rows": rows, "columns": column_names})
        results = [dict(zip(column_names, row)) for row in rows]

        logging.info("Query executed successfully, fetched %d rows", len(rows))
        print("results", results)
        return results

    except sqlite3.Error as e:
        logging.error("SQLite error: %s", e)
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info("Database connection closed")


@tool
def get_top_priority_leads(userInput: str):
    """

    Description: Provide List of top priority Leads list
    Fetch top lead details from the Leads table in the database.
    Fetch all lead details from the Leads table in the database.
    Fetch all Record in the table > tbody > tr > td > th formate

    Returns:
    provide the detail for the following columns: LeadID, FirstName, Amount, Email, Phone, CreatedBy
    dict: A dictionary containing all lead details fetched from the Leads table.
        The tool must return the output in the markdown structured.
         Tables should follow the format for: **table > tbody > tr > td > th**. ".
    """

    conn = None
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        logging.info("Connected to database")

        # Execute query to fetch all rows from Leads table
        query = "SELECT LeadID, FirstName, Amount, Email, Phone, CreatedBy, RatingId FROM Leads LIMIT 4 where RatingId > 2"
        logging.info("Executing query: %s", query)
        cursor.execute(query)

        # Fetch all rows and extract column names
        rows = cursor.fetchall()
        print("rows", rows)
        column_names = [column[0] for column in cursor.description]
        # results = convert_response_to_modal("table", {"rows": rows, "columns": column_names})
        results = [dict(zip(column_names, row)) for row in rows]

        logging.info("Query executed successfully, fetched %d rows", len(rows))
        print("results", results)
        return results

    except sqlite3.Error as e:
        logging.error("SQLite error: %s", e)
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info("Database connection closed")


@tool
def get_lead_detail_by_id(leadid: str):
    """

    Description: Provide detail of lead by LeadID {leadid}
    Fetch lead details from the Leads table in the database.
    Fetch all lead details from the Leads table in the database.
    Fetch all Record in the ul > li or bullet form formate

    Parameters:
        LeadID (str): {leadid}.

    Returns:
    provide the detail for the following all columns available in the table.
    dict: A dictionary containing all lead details fetched from the Leads table.
        The tool must return the output in the markdown structured.
         Tables should follow the format for: **ul> li, ol> li, **Title**: Value **. ".
    """

    conn = None
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        logging.info("Connected to database")

        # Execute query to fetch all rows from Leads table
        query = "SELECT * FROM Leads where LeadID = " + leadid
        logging.info("Executing query: %s", query)
        cursor.execute(query)

        # Fetch all rows and extract column names
        rows = cursor.fetchall()
        print("rows", rows)
        column_names = [column[0] for column in cursor.description]
        # results = convert_response_to_modal("table", {"rows": rows, "columns": column_names})
        results = [dict(zip(column_names, row)) for row in rows]

        logging.info("Query executed successfully, fetched %d rows", len(rows))
        print("results", results)
        return results

    except sqlite3.Error as e:
        logging.error("SQLite error: %s", e)
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info("Database connection closed")


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
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
tools = [
    get_all_lead_details,
    get_all_actionable_leads,
    get_top_priority_leads,
    get_lead_detail_by_id,
    validate_markdown,
]

tools_next = [
    get_all_lead_details,
    get_all_actionable_leads,
    get_top_priority_leads,
    get_lead_detail_by_id,
    validate_markdown,
]

model = next_llm.get_acidaes_llm_with_tool(tools)


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
# user_input = input("Enter your question about leads: ")

user_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a database expert with 15 years of experience in managing, leading, and providing accurate information. Your task is to use the provided tools to search for lead details, top leads, follow-up information, and priority leads. You must return responses in a structured markdown format, adhering to the tool descriptions."
            "Always format responses using proper markdown syntax, including code blocks, bullet points, and tables where applicable."
            "Note: Prioritize using the tools provided to fetch the required information.",
        ),
        ("placeholder", "{messages}"),
    ]
)

assistant_runnable = user_prompt | model

# print("assistant_runnable", assistant_runnable)


builder = StateGraph(State)

builder.add_node("assistant", Assistant(assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

memory = MemorySaver()

app = builder.compile(checkpointer=memory)

# result = app.invoke({"messages": [HumanMessage(content=user_input)]}, config={"configurable": {"thread_id": 42}})

# print("res", result.messages[-1].content)

import uuid

thread_id = str(uuid.uuid4())

db_file = "src/sales_assistant/databse-sqllite/Lead.sqlite"

config = {
    "configurable": {
        # The passenger_id is used in our flight tools to
        # fetch the user's flight information\
        # Checkpoints are accessed by thread_id
        "thread_id": thread_id,
    }
}

# for event in events:
#     _print_event(event, _printed)
# from custom_tools.util import convert_markdown_to_json


def start_app(msg):
    # print("msg", msg)

    # return msg
    messages = app.invoke({"messages": [("user", msg.message)]}, config)
    message = messages.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]

    return message


# result = start_app()

# print("events", result)
