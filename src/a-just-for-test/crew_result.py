
from crewai import Process, Crew
from agent import senior_blog_writer, reseracher
from task import research_task, write_blog_task


my_crew = Crew(
    agents=[
        reseracher,
        senior_blog_writer
        
    ],
    tasks=[
        research_task,
        write_blog_task
    ],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    sharp_crew=True
)

def kickoff(topic:str):
    my_crew.memory = topic
    return my_crew.kickoff(inputs={"topic":topic})