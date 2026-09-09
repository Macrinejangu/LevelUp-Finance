"""
This file connects our Python code to the SQLite database.

It has two jobs:
1. Open a connection to the database file (get_connection)
2. Create all the tables the first time the app runs (init_db)
"""
import sqlite3
import os

DB_PATH = "levelup_finance.db"


def get_connection():
    # This opens the database file. If it doesn't exist yet,
    # SQLite creates it automatically.
    conn = sqlite3.connect(DB_PATH)

    # By default, SQLite does NOT check that foreign keys are valid.
    # That means it would normally let us save a transaction pointing
    # to an account_id that doesn't exist, without warning us.
    # This line turns that checking on, so mistakes like that get caught.
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def init_db():
    # This function builds our tables using the instructions written
    # in schema.sql. It only needs to run once, but it's safe to run
    # every time the app starts, it won't break anything if the tables
    # already exist.

    # Step 1: find where schema.sql is saved.
    # This file (database.py) is inside the levelup folder.
    # schema.sql is one folder up, in the main project folder.
    current_folder = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_folder)
    schema_path = os.path.join(project_root, "schema.sql")

    # Step 2: open schema.sql and read its contents as plain text.
    # At this point it's just words on a page, nothing has happened yet.
    with open(schema_path, "r") as f:
        schema_sql = f.read()

    # Step 3: connect to the database and run all those SQL commands.
    conn = get_connection()
    conn.executescript(schema_sql)

    # Step 4: save the changes. Without this line, the tables would
    # only exist temporarily and disappear once the connection closes.
    conn.commit()

    # Step 5: close the connection. Always close it once you're done,
    # leaving it open can cause problems later.
    conn.close()

    print("Database initialized, all tables ready.")


 

# --------------------------------------------------
# ACCOUNT FUNCTIONS
# --------------------------------------------------

def add_account(name, account_type, balance=0):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO accounts (name, type, balance)
        VALUES (?, ?, ?)
    """, (name, account_type, balance))

    account_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return account_id


def get_account(account_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM accounts
        WHERE id = ?
    """, (account_id,))

    account = cursor.fetchone()

    conn.close()

    return account


def get_all_accounts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM accounts
        ORDER BY id
    """)

    accounts = cursor.fetchall()

    conn.close()

    return accounts


def update_balance(account_id, balance):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE accounts
        SET balance = ?
        WHERE id = ?
    """, (balance, account_id))

    conn.commit()
    conn.close()


# --------------------------------------------------
# TRANSACTION / LEDGER FUNCTIONS
# --------------------------------------------------

def add_transaction(account_id, amount, category, date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (account_id, amount, category, date)
        VALUES (?, ?, ?, ?)
    """, (account_id, amount, category, date))

    transaction_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return transaction_id


def get_transactions(account_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM transactions
        WHERE account_id = ?
        ORDER BY date DESC
    """, (account_id,))

    transactions = cursor.fetchall()

    conn.close()

    return transactions


def get_transactions_by_date(
    account_id,
    start_date=None,
    end_date=None
):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT *
        FROM transactions
        WHERE account_id = ?
    """

    parameters = [account_id]

    if start_date:
        query += " AND date >= ?"
        parameters.append(start_date)

    if end_date:
        query += " AND date <= ?"
        parameters.append(end_date)

    query += " ORDER BY date DESC"

    cursor.execute(query, parameters)

    transactions = cursor.fetchall()

    conn.close()

    return transactions


def get_total_by_category(account_id, category):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE account_id = ?
        AND category = ?
    """, (account_id, category))

    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        return 0

    return total


# --------------------------------------------------
# RUN DATABASE INITIALIZATION
# --------------------------------------------------   


# Run this file directly to set up the database:
# python3 -m levelup.database
if __name__ == "__main__":
    init_db()
