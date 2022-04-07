import os
import sqlite3
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    pass

DB_FILENAME = os.getenv("DB_FILENAME") or "trip_tracker.sqlite"
DB_FILE_PATH = os.path.join(dirname, "..", "data", DB_FILENAME)

connection = sqlite3.connect(DB_FILE_PATH)
connection.row_factory = sqlite3.Row


def get_db_connection():
    return connection
