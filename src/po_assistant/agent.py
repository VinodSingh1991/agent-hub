import os
from langgraph import Agent  # Assuming LangGraph has an equivalent Agent class
from dotenv import load_dotenv
from textwrap import dedent
from src.po_assistant.custom_tool.browser_tools import BrowserTools
from src.po_assistant.custom_tool.search_tools import SearchTools
from src.po_assistant.custom_tool.website_search import CustomWebSearchTool
from langgraph_tools import FileReadTool, SerperDevTool, WebsiteSearchTool, YoutubeVideoSearchTool, FirecrawlSearchTool  # Assuming LangGraph has these or similar tool modules
from src.llm_factory.acidaes_llm import next_llm

load_dotenv()

# Initialize the LLM
llm = next_llm.get_open_ai_llm()

# Initialize tools
file_tool = FileReadTool()
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()
youtube = YoutubeVideoSearchTool()
firecrawl = FirecrawlSearchTool(api_key=os.getenv("FILE_CROWL_API_KEY"))

# Agent Definitions
product_manager = Agent(
    role="Product Manager",
    goal=dedent("""
        Identify and analyze the top competition products in the market to compile a comprehensive list of 
        10 features that are both unique and highly valuable to customers. Use these insights to recommend 
        innovative improvements and strategic adjustments for the company’s product offerings, and reflect 
        on whether the resources are valuable or not.
    """),
    backstory=dedent("""
        As a seasoned Product Manager with a decade of experience in the tech industry, you have a keen eye for
        identifying market trends and customer needs. Your expertise lies in dissecting competitors' products, 
        extracting key insights, and leveraging this information to enhance your own products. Equipped with advanced 
        analytical tools and a strategic mindset, you are now tasked with staying ahead of the competition by identifying 
        unique and high-value features for integration into the product line.
    """),
    tools=[
        SearchTools.search_internet,
        BrowserTools.scrape_and_summarize_website,
        youtube,
    ],
    allow_delegation=False,
    verbose=True,
    llm=llm
)

product_owner = Agent(
    role="Product Owner",
    goal=dedent("""
        Identify and analyze the top competition products in the market to compile a comprehensive list of 
        10 features that are both unique and highly valuable to customers. Use these insights to recommend 
        innovative improvements and strategic adjustments for the company’s product offerings.
    """),
    backstory=dedent("""
        As an experienced Product Owner, you bring a wealth of knowledge in product development and market analysis. 
        With a background in tech startups, you excel at identifying key features that differentiate successful products. 
        Your mission is to support the Product Manager by delivering detailed competitive analysis and feature 
        recommendations, ensuring the company's products remain innovative and meet customer needs.
    """),
    tools=[
        SearchTools.search_internet,
        BrowserTools.scrape_and_summarize_website,
        youtube,
    ],
    allow_delegation=False,
    verbose=True,
    llm=llm
)

solution_architect = Agent(
    role="CRM Solution Architect",
    goal=dedent("""
        Create a detailed product documentation that outlines solutions based on CRMNext components. 
        Consolidate solutions for each feature to provide the project manager with a comprehensive view of the product architecture.
    """),
    backstory=dedent("""
        With over 20 years as a CRM Solution Architect, you possess a deep understanding of CRM systems, including CRMNext. 
        You are known for your ability to clarify complex solutions and simplify documentation. You are tasked with creating 
        a comprehensive technical requirement documentation, leveraging CRMNext’s extensive components to achieve each product feature.
    """),
    tools=[
        CustomWebSearchTool.search,
    ],
    allow_delegation=False,
    verbose=True,
    max_itr=1,
    max_rpm=1,
    llm=llm
)

scrum_master = Agent(
    role="Project Manager",
    goal=dedent("""
        Develop a comprehensive Technical Requirement Document (TRD) to outline solutions for CRMNext-based components. 
        Include sections for objectives, feature lists, implementation, test cases, deployment checklist, and estimated efforts.
    """),
    backstory=dedent("""
        With over two decades of experience as a CRM Solution Architect, you possess an in-depth understanding of CRM platforms. 
        Your role now is to create a Technical Requirement Document (TRD) for the CRMNext-based components of the project, 
        outlining clear objectives, implementation steps, testing, deployment, and time estimates.
    """),
    tools=[
         CustomWebSearchTool.search,
    ],
    allow_delegation=False,
    verbose=True,
    max_itr=1,
    max_rpm=1,
    llm=llm
)
