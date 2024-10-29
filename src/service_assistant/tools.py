import sqlite3
import logging
import re

from langchain_core.tools import tool
from src.service_assistant.db_query import (
    GET_ACTION_ABLE_LEADS,
    GET_TOP_PRIORITY_LEADS,
    GET_ALL_ACCOUNTS,
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


def fetch_all_accounts():
    """
    Fetch all Account Information details including Cases, offers.

    Args:
        userInput (str): User input (not actively used in this function).

    Returns:
        list[dict]: A list of dictionaries containing Account information in Detail, with all columns from the database.:


    Notes:
        Use this tool to retrieve an overview of all available leads in the database.
        the response should be on table tr th, table tr td with valid markdown.
        the response should be on table tr td th formate with valid markdown.
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        logging.info("Connected to database")
        query = GET_ALL_ACCOUNTS
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


def generate_email(account):
    return f"""
    Subject: Exclusive Offer on {account['OfferName']} Just for You!

    Dear {account['FirstName']} {account['LastName']},

    We’re excited to inform you about an exclusive offer on our {account['OfferName']} tailored especially for you! 
    Here’s what’s included:

    - **Offer Criteria:** {account['OfferCriteria']}
    - **Minimum Income Required:** {account['MinIncome']}

    ### Related Cases:
    | Case Subject  | Status    |
    |---------------|-----------|
    | {account['CaseSubject']} | {account['CaseStatus']} |

    This offer is valid only for a limited time. If you would like to apply or have any questions, please feel free to reach out to us.

    We look forward to welcoming you to a world of exclusive privileges and rewarding experiences.

    Warm Regards,
    [Your Bank’s Name] Customer Service Team
    """


tools_next = [
    fetch_all_accounts,
    validate_markdown,
]


db_file = "src/service_assistant/databse-sqllite/Lead.sqlite"
