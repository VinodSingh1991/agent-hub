import os
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool

web_scrap_tool = ScrapeWebsiteTool()
search_tool = SerperDevTool()
web_search_tool = WebsiteSearchTool()