
from crewai import Task
from textwrap import dedent

class PagTask():
    def identify_task(self, agent, topic):
        return Task(
            description=dedent(f"""
            Gather the information on the topic {topic}.
            Gather the pros and cons of the {topic}.
            """),
            agent=agent,
            expected_output="Detailed report on the chosen city including flight costs, weather forecast, and attractions"
        )
        
    
    def blog_writing(self, agent, topic):
        return Task(
            description=dedent(f"""
            Gather the information on the topic {topic}.
            Gather the pros and cons of the {topic}.
            """),
            agent=agent,    
            expected_output=dedent(f"""Write a blog post on the {topic} with pros and cons for {topic}.
The blog post should be informative and engaging for readers, at least 500 words long, well-researched,
and include references to credible sources.""")
        )