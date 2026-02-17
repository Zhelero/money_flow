from models import Expense
import sqlite3

DB_NAME = 'expenses.db'

class ExpenseRepository:
    def __init__(self):
        self._init_db()

    def _connect(self):
        return sqlite3.connect(DB_NAME)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS expenses(
                deal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                money_source TEXT,
                category TEXT,
                created_at TEXT
                )
            ''')

    def load(self):
        with self._connect() as conn:
            cursor = conn.execute('SELECT * FROM expenses')
            rows = cursor.fetchall()
        return [
            Expense(deal_id=row[0], amount=row[1], money_source=row[2], category=row[3], created_at=row[4]) for row in rows
        ]


    def spend(self, expense: Expense):
        with self._connect() as conn:
            conn.execute("""
            INSERT INTO expenses (amount, money_source, category, created_at)
            VALUES (?, ?, ?, ?)
            """, (expense.amount, expense.money_source, expense.category, expense.created_at))

    def delete(self, deal_id) -> None:
        with self._connect() as conn:
            conn.execute("""DELETE FROM expenses WHERE deal_id = ?""", (deal_id,))

    def update(self, expense: Expense) -> None:
        with self._connect() as conn:
            conn.execute("""
                         UPDATE expenses 
                         SET amount = ?, money_source = ?, category = ?, created_at = ?
                         WHERE deal_id = ?
                         """, (expense.amount, expense.money_source, expense.category, expense.created_at, expense.deal_id))

    def total(self, category=None):
        with self._connect() as conn:
            if category:
                cursor = conn.execute(
                    "SELECT SUM(amount) FROM expenses WHERE category = ?",
                    (category,)
                )
            else:
                cursor = conn.execute("SELECT SUM(amount) FROM expenses")

            result = cursor.fetchone()[0]
            return result if result is not None else 0

    def totals_by_category(self):
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT category, SUM(amount)
                FROM expenses
                GROUP BY category
            """)
            return cursor.fetchall()


