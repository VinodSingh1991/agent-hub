import os
from dotenv import load_dotenv
from typing import Annotated
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool

# Define the tools to be used in the application
load_dotenv()
travily_search_api = os.getenv("TAVILY_API_KEY")
tavily_tool = TavilySearchResults(api_key=travily_search_api, max_results=5)
python_repl = PythonREPLTool()

#coding_tools = [tavily_tool, python_repl]