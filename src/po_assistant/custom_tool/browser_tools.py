import json
import os
import requests
from langgraph import Agent, Task  # Assuming LangGraph has similar classes
from langchain.tools import tool
from unstructured.partition.html import partition_html


class BrowserTools:

    @tool("Scrape website content")
    def scrape_and_summarize_website(website):
        """Useful to scrape and summarize a website content"""
        url = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
        payload = json.dumps({"url": website})
        headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        
        # Partition the HTML into elements
        elements = partition_html(text=response.text)
        content = "\n\n".join([str(el) for el in elements])
        
        # Chunk content if needed for summary processing
        content_chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        summaries = []
        
        # Iterate over content chunks and create tasks for each
        for chunk in content_chunks:
            # Replace Crew AI's Agent and Task with LangGraph equivalents
            agent = Agent(
                role='Principal Researcher',
                goal='Conduct high-quality research and produce summaries from content provided.',
                backstory="You are a principal researcher tasked with summarizing large amounts of content.",
                allow_delegation=False
            )
            task = Task(
                agent=agent,
                description=f'Please analyze and summarize the content below. Only return the summary:\n\nCONTENT\n----------\n{chunk}'
            )
            summary = task.execute()  # Execute task in LangGraph
            summaries.append(summary)
        
        # Join summaries into a single text output
        return "\n\n".join(summaries)
