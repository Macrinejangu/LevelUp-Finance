"""
SQLite connection helpers.
→ Schema lives in schema.sql at the project root.
→ Foreign key enforcement is off by default in SQLite, turned on manually below.
"""
import sqlite3

DB_PATH = "levelup_finance.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# → run schema.sql against a fresh database
def init_db():
    pass
