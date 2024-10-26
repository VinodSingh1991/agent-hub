from langchain_core.tools import tool
from src.sales_assistant.database import LeadDatabase

class LeadTools:
    """
    A collection of tools to interact with lead data in the database.
    This class provides methods for retrieving all leads, actionable leads,
    top-priority leads, and specific lead details by LeadID.
    """

    def __init__(self):
        # Initialize LeadDatabase instance
        self.db = LeadDatabase()

    @tool
    def get_all_lead_details(self, userInput: str):
        """
        Fetch all lead details.

        Args:
            userInput (str): User input (not actively used in this function).

        Returns:
            list[dict]: A list of dictionaries containing lead details, with keys such as:
                - LeadID: Unique identifier for the lead.
                - FirstName: First name of the lead.
                - Amount: Associated amount for the lead.
                - Email: Contact email of the lead.
                - Phone: Contact phone number of the lead.
                - CreatedBy: Creator of the lead record.

        Notes:
            Use this tool to retrieve an overview of all available leads in the database.
            the response should be on ul>li, ol> li with valid markdown.
            the response should be on table tr td th formate with valid markdown.
        """

        print(self.db.fetch_all_leads())

        return self.db.fetch_all_leads()

    @tool
    def get_all_actionable_leads(self, userInput: str):
        """
        Fetch actionable leads based on defined criteria (e.g., high-priority leads).

        Args:
            userInput (str): User input (not actively used in this function).

        Returns:
            list[dict]: A list of dictionaries containing actionable lead details, filtered to
                meet specific conditions. Fields include:
                - LeadID: Unique identifier for the lead.
                - FirstName: First name of the lead.
                - Amount: Associated amount for the lead, generally above a threshold.
                - Email: Contact email of the lead.
                - Phone: Contact phone number of the lead.
                - CreatedBy: Creator of the lead record.

        Notes:
            Useful for extracting leads that require immediate attention, such as those
            with significant associated amounts or other prioritization markers.
            the response should be on table tr td th formate with valid markdown.
        """
        return self.db.fetch_actionable_leads()

    @tool
    def get_top_priority_leads(self, userInput: str):
        """
        Retrieve top-priority leads based on rating and other prioritization metrics.

        Args:
            userInput (str): User input (not actively used in this function).

        Returns:
            list[dict]: A list of dictionaries containing top-priority lead details, limited to
                a specified number of high-rated entries. Fields include:
                - LeadID: Unique identifier for the lead.
                - FirstName: First name of the lead.
                - Amount: Associated amount for the lead.
                - Email: Contact email of the lead.
                - Phone: Contact phone number of the lead.
                - CreatedBy: Creator of the lead record.
                - RatingId: Numeric rating identifier for lead prioritization.

        Notes:
            Designed for cases where only the highest priority leads are needed.
            the response should be on table tr td th formate with valid markdown.
        """
        return self.db.fetch_top_priority_leads()

    def get_lead_detail_by_id(self, leadid: str):
        """
        Fetch detailed information for a specific lead by LeadID.

        Args:
            leadid (str): The unique identifier of the lead to retrieve.

        Returns:
            dict: A dictionary with detailed information about the lead, including:
                - LeadID: Unique identifier for the lead.
                - FirstName: First name of the lead.
                - Amount: Associated amount for the lead.
                - Email: Contact email of the lead.
                - Phone: Contact phone number of the lead.
                - CreatedBy: Creator of the lead record.
                - Other available columns in the lead table.

        Notes:
            Ideal for retrieving comprehensive information on a particular lead, based on its ID.
            All columns available in the Leads table are included in the response.
            the response should be on ul>li, ol> li with valid markdown.
        """
        return self.db.fetch_lead_by_id(leadid)
