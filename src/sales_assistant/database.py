import sqlite3
import logging
from src.sales_assistant.config import DB_FILE

class LeadDatabase:
    def __init__(self):
        self.db_file = "src/sales_assistant/database-sqllite/Lead.sqlite"

    def get_connection(self):
        """Establish a connection to the SQLite database."""

        print(self.db_file, "self.db_file")
        try:
            conn = sqlite3.connect(self.db_file)
            logging.info("Connected to database")
            return conn
        except sqlite3.Error as e:
            logging.error("Database connection error: %s", e)
            return None

    def fetch_all_leads(self):
        """Fetch all leads with specific columns from the Leads table."""
        query = "SELECT LeadID, FirstName, Amount, Email, Phone, CreatedBy FROM Leads"
        return self._execute_query(query)

    def fetch_actionable_leads(self):
        """Fetch leads where Amount > 200 from the Leads table."""
        query = "SELECT LeadID, FirstName, Amount, Email, Phone, CreatedBy FROM Leads WHERE Amount > 200"
        return self._execute_query(query)

    def fetch_top_priority_leads(self):
        """Fetch top priority leads (RatingId > 2, limited to 4) from the Leads table."""
        query = """
            SELECT LeadID, FirstName, Amount, Email, Phone, CreatedBy, RatingId 
            FROM Leads WHERE RatingId > 2 LIMIT 4
        """
        return self._execute_query(query)

    def fetch_lead_by_id(self, lead_id):
        """Fetch lead details by specific LeadID from the Leads table."""
        query = f"SELECT * FROM Leads WHERE LeadID = '{lead_id}'"
        return self._execute_query(query)

    def _execute_query(self, query):
        """Helper method to execute a query and fetch results."""
        conn = self.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            print(column_names, rows)
            return [dict(zip(column_names, row)) for row in rows]
        except sqlite3.Error as e:
            logging.error("SQL error: %s", e)
            return []
        finally:
            logging.error("SQL conn failed: %s", e)
            cursor.close()
            conn.close()
