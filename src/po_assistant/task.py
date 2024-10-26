from crewai import Task
from tools import search_tool, web_search_tool, web_scrap_tool
from agent import reseracher, senior_blog_writer

# Creating a Senior researcher task
research_task = Task(
    description=(
        "Identify the most recent and next big trends topic on the AI and Machine Learning {topic}. "
        "Get the pros and cons of the trends."
    ),
    expected_output= "A 3-paragraph report on the most recent and next big trends in the field of AI with pros and cons for {topic}.",
    tools=[search_tool, web_search_tool, web_scrap_tool],
    agent=reseracher
)

# Creating a Senior blog writer task
write_blog_task = Task(
    description=(
        "Get the information from {topic} on the topic {topic}."
    ),
    expected_output="""Write a blog post on the most recent and next big trends in the field of AI with pros and cons for {topic}.
The blog post should be informative and engaging for readers, at least 1000 words long, well-researched,
and include references to credible sources.""",
    tools=[search_tool],
    agent=senior_blog_writer,
    async_execution=False,
    output_file="researcher-agent/blog_post.txt"
)
