import sqlite3
import logging
import re

from langchain_core.tools import tool
from src.sales_assistant.db_query import (
    GET_ALL_LEADS,
    GET_ACTION_ABLE_LEADS,
    GET_TOP_PRIORITY_LEADS,
)


# Initialize logging (this can be configured more globally)
logging.basicConfig(level=logging.INFO)


@tool
def validate_markdown(message: str):
    """
    Removes markdown-style code block delimiters (```) and the ```markdown``` pattern from a given string.

    Args:
        message (str): The input string that may contain triple backticks and markdown code blocks.

    Returns:
        str: The string with all markdown code block delimiters and ```markdown``` patterns removed.

    Notes:
        - The tool must return the output in markdown structure.
        - The output format should not be changed beyond removing the markdown-style delimiters.
    """

    return re.sub(r"```markdown|```", "", message) if message else ""


@tool
def get_all_lead_details(userInput: str):
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

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        logging.info("Connected to database")
        query = GET_ALL_LEADS
        logging.info("Executing query: %s", query)
        cursor.execute(query)

        rows = cursor.fetchall()
        print("rows", rows)
        column_names = [column[0] for column in cursor.description]
        results = [dict(zip(column_names, row)) for row in rows]

        logging.info("Query executed successfully, fetched %d rows", len(rows))
        print("results", results)
        return results

    except sqlite3.Error as e:
        logging.error("SQLite error: %s", e)
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info("Database connection closed")


@tool
def get_all_actionable_leads(userInput: str):
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

    conn = None
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        logging.info("Connected to database")

        # Execute query to fetch all rows from Leads table
        query = GET_ACTION_ABLE_LEADS
        logging.info("Executing query: %s", query)
        cursor.execute(query)

        # Fetch all rows and extract column names
        rows = cursor.fetchall()
        print("rows", rows)
        column_names = [column[0] for column in cursor.description]
        # results = convert_response_to_modal("table", {"rows": rows, "columns": column_names})
        results = [dict(zip(column_names, row)) for row in rows]

        logging.info("Query executed successfully, fetched %d rows", len(rows))
        print("results", results)
        return results

    except sqlite3.Error as e:
        logging.error("SQLite error: %s", e)
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info("Database connection closed")


@tool
def get_top_priority_leads(userInput: str):
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

    conn = None
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        logging.info("Connected to database")

        # Execute query to fetch all rows from Leads table
        query = GET_TOP_PRIORITY_LEADS
        logging.info("Executing query: %s", query)
        cursor.execute(query)

        # Fetch all rows and extract column names
        rows = cursor.fetchall()
        print("rows", rows)
        column_names = [column[0] for column in cursor.description]
        # results = convert_response_to_modal("table", {"rows": rows, "columns": column_names})
        results = [dict(zip(column_names, row)) for row in rows]

        logging.info("Query executed successfully, fetched %d rows", len(rows))
        print("results", results)
        return results

    except sqlite3.Error as e:
        logging.error("SQLite error: %s", e)
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info("Database connection closed")


@tool
def get_lead_detail_by_id(leadid: str):
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

    conn = None
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        logging.info("Connected to database")

        # Execute query to fetch all rows from Leads table
        query = f"SELECT * FROM Leads where LeadID = {leadid}"
        logging.info("Executing query: %s", query)
        cursor.execute(query)

        # Fetch all rows and extract column names
        rows = cursor.fetchall()
        print("rows", rows)
        column_names = [column[0] for column in cursor.description]
        # results = convert_response_to_modal("table", {"rows": rows, "columns": column_names})
        results = [dict(zip(column_names, row)) for row in rows]

        logging.info("Query executed successfully, fetched %d rows", len(rows))
        print("results", results)
        return results

    except sqlite3.Error as e:
        logging.error("SQLite error: %s", e)
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info("Database connection closed")


@tool
def get_column_sum(column_name: str):
    """
    Calculate the sum of a specified column/Field in the Leads table.

    Args:
        column_name (str): Name of the column to sum.

    Returns:
        float: Sum of the specified column.

    Notes:
        Ensure that the column contains numeric values.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        query = f"SELECT SUM({column_name}) FROM Leads"
        cursor.execute(query)
        return cursor.fetchone()[0] or 0
    except sqlite3.Error as e:
        logging.error("SQLite error: %s", e)
        return 0

    finally:
        if conn:
            cursor.close()
            conn.close()


@tool
def create_lead(
    FirstName: str,
    Amount: float,
    Email: str,
    Phone: str,
    CreatedBy: str,
    Address: str = None,
    City: str = None,
    State: str = None,
    PinCode: str = None,
    CreatedOn: str = None,
    Rating: str = None,
    LastName: str = None,
):
    """
    Create a new lead entry in the Leads table.

    Args:
        FirstName (str): First name of the lead.
        LastName (str): Last name of the lead.
        Phone (str): Phone of the lead.
        Email (str): Email of the lead.
        Address (str): Address of the lead (optional).
        City (str): City of the lead (optional).
        State (str): State of the lead (optional).
        PinCode (str): PinCode of the lead (optional).
        CreatedOn (str): CreatedOn of the lead (optional).
        Amount (float): Amount of the lead.
        Rating (str): Rating of the lead (optional).
        CreatedBy (str): Creator of the lead.

    Returns:
        str: Success or failure message.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        query = """
        INSERT INTO Leads (FirstName, Amount, Email, Phone, CreatedBy, CreatedOn, RatingId, Address, City, State, PinCode, LastName) 
        VALUES (?, ?, ?, ?, ?, datetime('now'), ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(
            query,
            (
                FirstName,
                Amount,
                Email,
                Phone,
                CreatedBy,
                Rating,
                Address,
                City,
                State,
                PinCode,
                LastName,
            ),
        )
        conn.commit()
        return "Lead created successfully."

    except sqlite3.Error as e:
        logging.error("SQLite error: %s", e)
        return "Failed to create lead."

    finally:
        if conn:
            cursor.close()
            conn.close()


@tool
def update_lead(
    lead_id: int,
    first_name: str = None,
    last_name: str = None,
    phone: str = None,
    email: str = None,
    address: str = None,
    city: str = None,
    state: str = None,
    pin_code: str = None,
    created_on: str = None,
    amount: float = None,
    rating: str = None,
    created_by: str = None,
):
    """
    Update lead details in the Leads table.

    Args:
        lead_id (int): The Lead ID of the lead to update.
        first_name (str): First name of the lead (optional).
        last_name (str): Last name of the lead (optional).
        phone (str): Phone of the lead (optional).
        email (str): Contact email (optional).
        address (str): Address of the lead (optional).
        city (str): City of the lead (optional).
        state (str): State of the lead (optional).
        pin_code (str): PinCode of the lead (optional).
        created_on (str): CreatedOn date of the lead (optional).
        amount (float): Associated amount (optional).
        rating (str): Rating of the lead (optional).
        created_by (str): Creator of the lead record (optional).

    Returns:
        str: Success or failure message.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        updates = []
        params = []

        if first_name:
            updates.append("FirstName = ?")
            params.append(first_name)
        if last_name:
            updates.append("LastName = ?")
            params.append(last_name)
        if phone:
            updates.append("Phone = ?")
            params.append(phone)
        if email:
            updates.append("Email = ?")
            params.append(email)
        if address:
            updates.append("Address = ?")
            params.append(address)
        if city:
            updates.append("City = ?")
            params.append(city)
        if state:
            updates.append("State = ?")
            params.append(state)
        if pin_code:
            updates.append("PinCode = ?")
            params.append(pin_code)
        if created_on:
            updates.append("CreatedOn = ?")
            params.append(created_on)
        if amount is not None:  # Handle float comparison correctly
            updates.append("Amount = ?")
            params.append(amount)
        if rating:
            updates.append("RatingId = ?")
            params.append(rating)
        if created_by:
            updates.append("CreatedBy = ?")
            params.append(created_by)

        if updates:
            params.append(lead_id)
            query = f"UPDATE Leads SET {', '.join(updates)} WHERE LeadID = ?"
            cursor.execute(query, params)
            conn.commit()
            return "Lead updated successfully."

        return "No updates made."

    except sqlite3.Error as e:
        logging.error("SQLite error: %s", e)
        return "Failed to update lead."

    finally:
        if conn:
            cursor.close()
            conn.close()


tools_next = [
    get_all_lead_details,
    get_all_actionable_leads,
    get_top_priority_leads,
    get_lead_detail_by_id,
    get_column_sum,
    create_lead,
    update_lead,
    validate_markdown,
]


db_file = "src/sales_assistant/databse-sqllite/Lead.sqlite"
