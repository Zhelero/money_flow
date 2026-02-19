from models import Expense, Account
from exceptions import (AccountNotFoundError, NotEnoughMoneyError, AccountAlreadyExistsError)
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
            conn.execute('''
            CREATE TABLE IF NOT EXISTS accounts(
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                balance REAL
            )
            ''')

    def load(self):
        with self._connect() as conn:
            cursor = conn.execute('SELECT * FROM expenses')
            rows = cursor.fetchall()
        return [
            Expense(deal_id=row[0], amount=row[1], money_source=row[2], category=row[3], created_at=row[4]) for row in rows
        ]

    def get_by_id(self, deal_id):
        with self._connect() as conn:
            row = conn.execute(
                'SELECT * FROM expenses WHERE deal_id=?',
                (deal_id,)
            ).fetchone()
        return Expense(*row) if row else None

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
                cursor = conn.execute("SELECT SUM(amount) FROM expenses WHERE category = ?", (category,)
                )
            else:
                cursor = conn.execute("SELECT SUM(amount) FROM expenses")

            result = cursor.fetchone()[0]
            return result if result is not None else 0


class AccountRepository:
    def _connect(self):
        return sqlite3.connect(DB_NAME)

    def create_account(self, account: Account):
        try:
            with self._connect() as conn:
                conn.execute("""
                INSERT INTO accounts (name, balance)
                VALUES (?, ?)
                """, (account.name, account.balance))
        except sqlite3.IntegrityError:
            raise AccountAlreadyExistsError("Account already exists. Choose a different name.")

    def get_accounts(self):
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM accounts").fetchall()
            return [Account(*row) for row in rows]

    def update_balance(self, name, delta):
        with self._connect() as conn:
            cur = conn.execute("""
                SELECT balance FROM accounts WHERE name = ?
            """, (name,))

            row = cur.fetchone()
            if not row:
                raise AccountNotFoundError('Account not found')

            new_balance = row[0] + delta
            if new_balance < 0:
                raise NotEnoughMoneyError("Not enough money")

            conn.execute("""
                            UPDATE accounts 
                            SET balance = ?
                            WHERE name = ?
                        """, (new_balance, name))