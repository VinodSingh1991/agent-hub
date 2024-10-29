from crewai import Agent
from tools import search_tool, web_search_tool, web_scrap_tool
import os
from dotenv import load_dotenv
from crewai import LLM

from crewai import Agent
from langchain.llms import OpenAI

from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools


class TripAgents():

  def city_selection_agent(self):
    return Agent(
        role='City Selection Expert',
        goal='Select the best city based on weather, season, and prices',
        backstory=
        'An expert in analyzing travel data to pick ideal destinations',
        tools=[
            SearchTools.search_internet,
            BrowserTools.scrape_and_summarize_website,
        ],
        verbose=True)

  def local_expert(self):
    return Agent(
        role='Local Expert at this city',
        goal='Provide the BEST insights about the selected city',
        backstory="""A knowledgeable local guide with extensive information
        about the city, it's attractions and customs""",
        tools=[
            SearchTools.search_internet,
            BrowserTools.scrape_and_summarize_website,
        ],
        verbose=True)

  def travel_concierge(self):
    return Agent(
        role='Amazing Travel Concierge',
        goal="""Create the most amazing travel itineraries with budget and 
        packing suggestions for the city""",
        backstory="""Specialist in travel planning and logistics with 
        decades of experience""",
        tools=[
            SearchTools.search_internet,
            BrowserTools.scrape_and_summarize_website,
            CalculatorTools.calculate,
        ],
        verbose=True)


modal_name = "gpt-4o-mini"
temperature = 0

# Load the API key from the .env file
load_dotenv()

# Create the FastAPI app
apiKey = os.getenv("OPENAI_API_KEY")

if apiKey is None:
    print("API_KEY not found in .env file.")
else:
    print(f"API Key Loaded: {apiKey}")  # Check if the correct key is loaded (remove in production)

#this is openAi modal for the agent
llm = LLM(
    model=modal_name,
    api_key=apiKey
)

#llm = OpenAI(api_key=apiKey, default_headers={"content-type": "application/json", "user-agent": "OpenAI-Request"})

print ("LLM", llm)

#Creating a Senior researcher agent

reseracher = Agent(
    role="Senior AI and Machine Learning Researcher",
    name="Dr. Vinod",
    goal="Uncover groundbreaking research in the field of AI {topic}",
    backstory="Agent Vinod is a Senior Researcher at the Crew AI Research Institute. He has been working in the field of AI for over 10 years and has published numerous papers in top-tier conferences and journals. He is passionate about pushing the boundaries of AI research and is always on the lookout for new and exciting projects to work on. you explore and share your latest innovations in the field of AI.",
    verbose=True,
    memory=True,
    tools=[search_tool, web_search_tool, web_scrap_tool],
    allow_delegation=True,  
    llm=llm
)


#creating a senior blog writer agent in the field of AI and Machine Learning

senior_blog_writer = Agent(
    goal="Uncover groundbreaking research in the field of AI and write good blog {topic}",
    role="Senior AI and Machine Learning Blog Writer",
    name="Dr. Aayush",
    verbose=True,
    memory=True,
    backstory="Dr. Aayush is a Senior AI and Machine Learning Blog Writer at the Crew AI Research Institute. He has a passion for writing and has been writing about AI and Machine Learning for over 5 years. He is always on the lookout for new and exciting topics to write about and is dedicated to sharing his knowledge with the world.",
    allow_delegation=False,
    tools=[search_tool, web_search_tool, web_scrap_tool],
    llm=llm
)