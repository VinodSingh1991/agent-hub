from langgraph import Task  # Assuming LangGraph has a Task class
from textwrap import dedent

class ProductTask:
    """
    Base class for handling tasks related to product research, technical feasibility, and project planning.
    """

    def __init__(self, context):
        self.context = context

    def create_task(self, description, output_file, expected_output, agent):
        # Create a LangGraph Task
        return Task(
            description=dedent(description),
            agent=agent,
            output_file=output_file,
            expected_output=dedent(expected_output)
        )


class POResearchTask(ProductTask):
    """
    Task class for Product Owner Research to identify and evaluate top product features.
    """

    def execute(self, agent):
        """
        Executes the PO research task by creating a Task object that lists and reports on the top 10 unique features.

        Returns:
            Task: A Task object with a detailed report on the top 10 unique product features.
        """
        description = f"""
            Analyze and select the best product features based on specific requirements, 
            market availability, and competitor offerings. 
            
            Deliverable:
            - A list of the top 10 unique features, with descriptions that highlight the value to customers.
            - Identify tasks to accomplish these features and provide a detailed report on their implementation.
            
            Include all supporting resources (YouTube videos, blogs, competitor documentation) in an "Appendix" section.
            
            Basic product information:
            {self.context}
        """
        expected_output = """
            - 10 unique feature descriptions in bullet format.
            - Detailed comparison with competitors.
            - "Appendix" section with all relevant resource links.
        """
        return self.create_task(description, "po_research.md", expected_output, agent)


class TechnicalMeetingTask(ProductTask):
    """
    Task class for conducting a technical feasibility meeting to evaluate feature implementation within CRMNext.
    """

    def execute(self, agent):
        """
        Executes the technical feasibility task by creating a Task object analyzing feature implementation feasibility.

        Returns:
            Task: A Task object with solutions for implementing features in CRMNext.
        """
        description = f"""
            Analyze the feasibility and approach for implementing key features in the CRMNext platform. 
            Evaluate whether each feature can be implemented and describe the methods for integration.

            Basic product information:
            {self.context}
        """
        expected_output = "Solution descriptions for each feature to be implemented in the CRMNext platform."
        return self.create_task(description, "solution.md", expected_output, agent)


class ReadyForProjectTask(ProductTask):
    """
    Task class for creating a detailed two-month project plan to achieve product goals and implement identified features.
    """

    def execute(self, agent):
        """
        Executes the project planning task by creating a Task object with a two-month project timeline.

        Returns:
            Task: A Task object with a two-month project timeline and milestones.
        """
        description = f"""
            Develop a comprehensive two-month plan for achieving the product's goals and implementing core features.
            
            Deliverable:
            - A detailed project timeline with tasks, milestones, and deadlines.
            - Justification for task selection and prioritization.
            
            Basic product information:
            {self.context}
        """
        expected_output = """
            - A Technical Requirement document with detailed features and user stories.
            - Two-month project timeline with tasks, milestones, and deadlines.
        """
        return self.create_task(description, "project_plan.md", expected_output, agent)
