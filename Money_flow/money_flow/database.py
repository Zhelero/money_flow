import sqlite3
from .config import config

class Database:
    def __init__(self):
        self._init_db()

    def connect(self):
        conn = sqlite3.connect(config.DB_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        return conn

    def _init_db(self):
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS accounts(
                    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    balance REAL NOT NULL CHECK(balance >= 0)
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses(
                    deal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL CHECK(amount > 0),
                    money_source TEXT NOT NULL,
                    category TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (money_source) REFERENCES accounts(name)
                        ON DELETE RESTRICT
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_expenses_source
                ON expenses(money_source)
            """)

    def reset(self):
        with self.connect() as conn:
            conn.execute("DELETE FROM expenses")
            conn.execute("DELETE FROM accounts")
            conn.execute("DELETE FROM sqlite_sequence WHERE name = 'expenses'")
            conn.execute("DELETE FROM sqlite_sequence WHERE name = 'accounts'")

#Singleton instance
db_instance = Database()