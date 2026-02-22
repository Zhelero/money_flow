from .models import Expense, Account
from .exceptions import (AccountNotFoundError, NotEnoughMoneyError, AccountAlreadyExistsError, ExpenseNotFoundError)
from .config import config
import sqlite3


class ExpenseRepository:

    def _connect(self):
        return sqlite3.connect(config.DB_NAME, isolation_level=None)

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

        if not row:
            raise ExpenseNotFoundError("Expense not found")

        return Expense(*row)

    def spend_atomic(self, expense: Expense):
        with self._connect() as conn:
            try:
                cursor = conn.execute(
                    "SELECT balance FROM accounts WHERE name=?",
                    (expense.money_source,)
                )
                row = cursor.fetchone()

                if not row:
                    raise AccountNotFoundError("Account not found")

                new_balance = row[0] - expense.amount
                if new_balance < 0:
                    raise NotEnoughMoneyError("Not enough money")

                #Update balance
                conn.execute(
                    "UPDATE accounts SET balance=? WHERE name=?",
                    (new_balance, expense.money_source)
                )

                #Adding expense
                conn.execute("""
                INSERT INTO expenses (amount, money_source, category, created_at)
                VALUES (?, ?, ?, ?)
                """, (
                    expense.amount,
                    expense.money_source,
                    expense.category,
                    expense.created_at
                ))

            except:
                conn.rollback()
                raise

    def delete(self, deal_id) -> None:
        with self._connect() as conn:
            try:
                cursor = conn.execute(
                    "SELECT amount, money_source FROM expenses WHERE deal_id=?",
                    (deal_id,)
                )
                row = cursor.fetchone()
                if not row:
                    raise ExpenseNotFoundError("Expense not found")

                amount, money_source = row

                conn.execute(
                    "UPDATE accounts SET balance = balance + ? WHERE name=?",
                    (amount, money_source)
                )

                conn.execute(
                    """DELETE FROM expenses WHERE deal_id = ?""",
                    (deal_id,)
                )

            except Exception:
                conn.rollback()
                raise

            if cursor.rowcount == 0:
                raise ExpenseNotFoundError("Expense not found")

    def edit_atomic(self, expense: Expense, old_amount: float, old_source: str) -> None:
        with self._connect() as conn:
            try:
                #Check accounts existence
                cur = conn.execute(
                    "SELECT balance FROM accounts WHERE name=?",
                    (old_source,)
                )
                if not cur.fetchone():
                    raise AccountNotFoundError("Original account not found")

                cur = conn.execute(
                    "SELECT balance FROM accounts WHERE name=?",
                    (expense.money_source,)
                )
                if not cur.fetchone():
                    raise AccountNotFoundError("New account not found")

                #Update expense
                conn.execute("""
                    UPDATE expenses
                    SET amount= ?, money_source = ?, category = ?, created_at = ?
                    WHERE deal_id = ?
                """, (
                    expense.amount,
                    expense.money_source,
                    expense.category,
                    expense.created_at,
                    expense.deal_id
                ))

                if old_source == expense.money_source:
                    cur = conn.execute(
                        "SELECT balance FROM accounts WHERE name=?",
                        (expense.money_source,)
                    )
                    current_balance = cur.fetchone()[0]

                    delta = old_amount - expense.amount
                    new_balance = current_balance + delta

                    if new_balance < 0:
                        raise NotEnoughMoneyError("Not enough money for edit operation")

                    conn.execute(
                        "UPDATE accounts SET balance=? WHERE name=?",
                        (new_balance, expense.money_source)
                    )

                else:
                    #Check balance of new account
                    cur = conn.execute(
                        "SELECT balance FROM accounts WHERE name=?",
                        (expense.money_source,)
                    )
                    new_account_balance = cur.fetchone()[0]

                    if new_account_balance < expense.amount:
                        raise NotEnoughMoneyError("Not enough money in new account")

                    #Return old amount
                    conn.execute(
                        "UPDATE accounts SET balance = balance + ? WHERE name = ?",
                        (old_amount,old_source)
                    )

                    #Writing off new amount
                    conn.execute(
                        "UPDATE accounts SET balance = balance - ? WHERE name = ?",
                        (expense.amount, expense.money_source)
                    )

            except Exception:
                conn.rollback()
                raise

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
        return sqlite3.connect(config.DB_NAME)

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

    def transfer_atomic(self, from_acc: str, to_acc: str, amount: float):
        with self._connect() as conn:
            try:
                #Check sender
                cur = conn.execute(
                    "SELECT balance FROM accounts WHERE name = ?",
                    (from_acc,)
                )
                from_row = cur.fetchone()
                if not from_row:
                    raise AccountNotFoundError('Sender account not found')

                #Check receiver
                cur = conn.execute(
                    "SELECT balance FROM accounts WHERE name = ?",
                    (to_acc,)
                )
                to_row = cur.fetchone()
                if not to_row:
                    raise AccountNotFoundError('Receiver account not found')

                if from_row[0] < amount:
                    raise NotEnoughMoneyError("Not enough money")

                #Write off money from the account
                conn.execute(
                    "UPDATE accounts SET balance = balance - ? WHERE name = ?",
                    (amount, from_acc)
                )

                #Adding money to account
                conn.execute(
                    "UPDATE accounts SET balance = balance + ? WHERE name = ?",
                    (amount, to_acc)
                )

            except Exception:
                conn.rollback()
                raise