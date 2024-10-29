from crewai import Crew
from pag_assistant.pag_agent import PagAgent
from pag_assistant.pag_task import PagTask

class PagCrew:
    def __init__(self, topic):
        self.topic = topic
    
    def run(self):
        agents = PagAgent()
        tasks = PagTask()
       
        blog_reseracher = agents.researcher()
        blog_writer = agents.senior_blog_writer()
        
        blog_reseracher_task = tasks.identify_task(blog_reseracher, self.topic)
        blog_writer_task = tasks.blog_writing(blog_writer, self.topic)
        
        crew = Crew(
            agents=[blog_reseracher, blog_writer],
            tasks=[blog_reseracher_task, blog_writer_task],
            process="sequential",
            memory=True,
            cache=True,
            max_rpm=100,
            sharp_crew=True
        )
        
        result = crew.kickoff(inputs={"topic": self.topic})
        return result

def pag_crew_result(topic:str):
    my_crew = PagCrew(topic)
    return my_crew.run()
