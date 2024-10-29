import requests
from bs4 import BeautifulSoup
from langchain.tools import tool

class CustomWebSearchTool():
    """
    A tool to search and scrape data from the CrewAI documentation website.

    Methods:
        search(query: str) -> str:
            Searches the CrewAI documentation for the specified query and returns relevant content.
    """
    @tool
    def search(query: str) -> str:
        """
        Searches the CrewAI documentation for the specified query.

        Args:
            query (str): The search term to find in the documentation.

        Returns:
            str: A summary of the relevant documentation section, or a message indicating no results found.
        """
        url = "https://jsonplaceholder.typicode.com/"
        response = requests.get(url)

        if response.status_code != 200:
            return "Failed to retrieve documentation."

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find relevant content (customize this part based on actual HTML structure)
        results = soup.find_all('h2')  # Assuming the content is in <h2> tags
        if matches := [
            header.text
            for header in results
            if query.lower() in header.text.lower()
        ]:
            return f"Found the following matches for '{query}': " + ', '.join(matches)
        else:
            return f"No results found for '{query}'."

# Initialize the search tool
#website_tool = CustomWebSearchTool()
