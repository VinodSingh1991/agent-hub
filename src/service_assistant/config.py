import os
import logging
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

# Database path
DB_FILE = os.getenv("DB_FILE_PATH", "src/service_assistant/database-sqllite/Lead.sqlite")

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Optional: Add any other configuration constants here
