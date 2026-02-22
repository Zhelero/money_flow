import sqlite3
from .config import config

class Database:
    def __init__(self):
        self._init_db()

    def connect(self):
        return sqlite3.connect(config.DB_NAME)

    def _init_db(self):
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses(
                    deal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    money_source TEXT,
                    category TEXT,
                    created_at TEXT
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS accounts(
                    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    balance REAL NOT NULL CHECK(balance >= 0)
                )
            """)

    def reset(self):
        with self.connect() as conn:
            conn.execute("DELETE FROM expenses")
            conn.execute("DELETE FROM accounts")
            conn.execute("DELETE FROM sqlite_sequence WHERE name = 'expenses'")
            conn.execute("DELETE FROM sqlite_sequence WHERE name = 'accounts'")