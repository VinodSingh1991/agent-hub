from src.po_assistant.agent import product_manager, product_owner, scrum_master, solution_architect
from src.po_assistant.task import POResearchTask, TechnicalMeetingTask, ReadyForProjectTask
from crewai import Crew
class ProductActivationGroup:
    """
    This is a group of agents working together to achieve Product research and development
    for Businessnext platform.
    """

    def __init__(self, topic):
        self.topic = topic

    def run(self):

        #agents list

        agents = [product_manager, product_owner, scrum_master, solution_architect]
        pm_reasearch_task = POResearchTask(self.topic).execute(product_manager)
        po_reasearch_task = POResearchTask(self.topic).execute(product_manager)
        technical_meeting_task = TechnicalMeetingTask(self.topic).execute(solution_architect)
        ready_for_project_task = ReadyForProjectTask(self.topic).execute(scrum_master)

        agent_tasks = [pm_reasearch_task, po_reasearch_task, technical_meeting_task, ready_for_project_task]

        crew = Crew(
            agents=agents,
            tasks=agent_tasks,
            process="sequential",
            memory=True,
            cache=True,
            max_rpm=100,
            sharp_crew=True
        )

        return crew.kickoff(inputs={"topic": self.topic})
    

def po_start_app(topic:str):
    my_crew = ProductActivationGroup(topic)
    return my_crew.run()
