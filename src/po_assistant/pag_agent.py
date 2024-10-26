import os
from crewai import Agent
from pag_assistant.tools import search_tool, web_search_tool, web_scrap_tool
from llm_factory.llm_getter import get_openai_base_llm

class PagAgent:
    
    def __init__(self):
        # Initialize the language model with specified base URL and parameters
        self.llm = get_openai_base_llm()
    
    def researcher(self):
        """Create and return a research-focused agent with specific tools and goals."""
        return Agent(
            name="Dr James",
            role="Senior Researcher",
            goal="Uncover groundbreaking research in the field of {topic}.",
            backstory="""
                Dr James is a Senior Researcher and expert at the Oxford University Research Institute. 
                With over 10 years in groundbreaking research, he has published numerous papers in top-tier 
                conferences and journals. He is passionate about pushing research boundaries and is always 
                on the lookout for new and exciting projects.
            """,
            tools=[
                search_tool,
                web_search_tool,
                web_scrap_tool
            ],
            llm=self.llm,
            verbose=True
        )
        
    def senior_blog_writer(self):
        """Create and return a blog-writing-focused agent with specific tools and goals."""
        return Agent(
            name="Dr Aayush",
            role="Senior Blog Writer",
            goal="Create a well-formatted, high-quality blog post on {topic}.",
            backstory="""
                Dr Aayush is a Senior Blog Writer and expert at the Oxford University Research Institute. 
                He has been engaged in groundbreaking research for over a decade and published in top-tier 
                conferences and journals. His passion lies in delivering engaging and insightful blog content.
            """,
            tools=[
                search_tool,
                web_search_tool,
                web_scrap_tool
            ],
            llm=self.llm,
            verbose=True
        )