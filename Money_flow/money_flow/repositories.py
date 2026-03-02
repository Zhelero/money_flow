from .models import Expense, Account
from .exceptions import (AccountNotFoundError, NotEnoughMoneyError, AccountAlreadyExistsError, ExpenseNotFoundError)
from .database import Database
import sqlite3

class ExpenseRepository:
    def __init__(self, db: Database):
        self._db = db

    def _connect(self):
        return self._db.connect()

    def load(self):
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM expenses").fetchall()
        return [
            Expense(
                deal_id=row["deal_id"],
                amount=row["amount"],
                money_source=row["money_source"],
                category=row["category"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def get_by_id(self, deal_id):
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM expenses WHERE deal_id=?",
                (deal_id,)
            ).fetchone()

        if not row:
            raise ExpenseNotFoundError()

        return Expense(
            deal_id=row["deal_id"],
            amount=row["amount"],
            money_source=row["money_source"],
            category=row["category"],
            created_at=row["created_at"],
        )

    def by_category(self, category):
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM expenses WHERE category=?",
                (category,)
            ).fetchall()
            return [
                Expense(
                    deal_id=row["deal_id"],
                    amount=row["amount"],
                    money_source=row["money_source"],
                    category=row["category"],
                    created_at=row["created_at"],
                )
                for row in rows
            ]

    def spend_atomic(self, expense: Expense):
        with self._connect() as conn:
            cur = conn.cursor()

            #Get balance
            cur.execute(
                "SELECT balance FROM accounts WHERE name=?",
                (expense.money_source,)
            )
            row = cur.fetchone()
            if not row:
                raise AccountNotFoundError()

            current_balance = row["balance"]
            if current_balance < expense.amount:
                raise NotEnoughMoneyError()

            #Write off amount
            cur.execute(
                "UPDATE accounts SET balance= balance - ? WHERE name=?",
                (expense.amount, expense.money_source)
            )

            #Adding expense
            cur.execute("""
            INSERT INTO expenses (amount, money_source, category, created_at)
            VALUES (?, ?, ?, ?)
            """, (
                expense.amount,
                expense.money_source,
                expense.category,
                expense.created_at
            ))

    def delete(self, deal_id) -> None:
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT amount, money_source FROM expenses WHERE deal_id=?",
                (deal_id,)
            )
            row = cur.fetchone()
            if not row:
                raise ExpenseNotFoundError()

            amount = row["amount"]
            money_source = row["money_source"]

            cur.execute(
                "UPDATE accounts SET balance = balance + ? WHERE name=?",
                (amount, money_source)
            )

            if cur.rowcount == 0:
                raise AccountNotFoundError()

            cur.execute(
                """DELETE FROM expenses WHERE deal_id = ?""",
                (deal_id,)
            )

    def edit_atomic(
            self,
            deal_id: int,
            amount: float | None = None,
            money_source: str | None = None,
            category: str | None = None
    ) -> None:
        with self._connect() as conn:
            cur = conn.cursor()

            # Get current operation
            cur.execute(
                "SELECT amount, money_source, category, created_at FROM expenses WHERE deal_id=?",
                (deal_id,)
            )
            row = cur.fetchone()

            if not row:
                raise ExpenseNotFoundError()

            old_amount = row["amount"]
            old_source = row["money_source"]
            old_category = row["category"]

            #Get new values
            new_amount = amount if amount is not None else old_amount
            new_source = money_source if money_source is not None else old_source
            new_category = category if category is not None else old_category

            # Check existence of old account
            cur.execute(
                "SELECT balance FROM accounts WHERE name=?",
                (old_source,)
            )
            if not cur.fetchone():
                raise AccountNotFoundError("Old account not found")

            #Check existence of new account
            cur.execute(
                "SELECT balance FROM accounts WHERE name=?",
                (new_source,)
            )
            new_account_row = cur.fetchone()
            if not new_account_row:
                raise AccountNotFoundError("New account not found")

            #Account doesn't change
            if old_source == new_source:
                diff = new_amount - old_amount

                if diff > 0 and new_account_row["balance"] < diff:
                    raise NotEnoughMoneyError()

                cur.execute(
                    "UPDATE accounts SET balance = balance - ? WHERE name=?",
                    (diff, old_source)
                )

            #Account change
            else:
                # Return old amount
                cur.execute(
                    "UPDATE accounts SET balance= balance + ? WHERE name=?",
                    (old_amount, old_source)
                )

                #Check balance of new account
                if new_account_row["balance"] < new_amount:
                    raise NotEnoughMoneyError()

                #Write off new amount
                cur.execute(
                    "UPDATE accounts SET balance = balance - ? WHERE name=?",
                    (new_amount, new_source)
                )

            #Update expense
            cur.execute("""
                UPDATE expenses
                SET amount=?, money_source=?, category=?
                WHERE deal_id=?
            """, (
                new_amount,
                new_source,
                new_category,
                deal_id
            ))

    def total(self, category=None):
        with self._connect() as conn:
            if category:
                cur = conn.execute("SELECT COALESCE(SUM(amount), 0) AS total FROM expenses WHERE category = ?", (category,)
                )
            else:
                cur = conn.execute("SELECT COALESCE(SUM(amount), 0) AS total FROM expenses")

            return cur.fetchone()["total"]


class AccountRepository:
    def __init__(self, db: Database):
        self._db = db

    def _connect(self):
        return self._db.connect()

    def create_account(self, account: Account):
        try:
            with self._connect() as conn:
                conn.execute("""
                INSERT INTO accounts (name, balance)
                VALUES (?, ?)
                """, (account.name, account.balance))
        except sqlite3.IntegrityError:
            raise AccountAlreadyExistsError()

    def get_accounts(self):
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM accounts").fetchall()
            return [
                Account(
                    account_id=row["account_id"],
                    name=row["name"],
                    balance=row["balance"]
                ) for row in rows
            ]

    def update_balance(self, name, delta):
        with self._connect() as conn:
            cur = conn.execute("""
                SELECT balance FROM accounts WHERE name = ?
            """, (name,))

            row = cur.fetchone()
            if not row:
                raise AccountNotFoundError()

            new_balance = row["balance"] + delta
            if new_balance < 0:
                raise NotEnoughMoneyError()

            conn.execute("""
                            UPDATE accounts 
                            SET balance = ?
                            WHERE name = ?
                        """, (new_balance, name))

            return new_balance

    def transfer_atomic(self, from_acc: str, to_acc: str, amount: float):
        with self._connect() as conn:
            #Check old account
            cur = conn.execute(
                "SELECT balance FROM accounts WHERE name = ?",
                (from_acc,)
            )
            from_row = cur.fetchone()
            if not from_row:
                raise AccountNotFoundError("Old account not found")

            #Check new account
            cur = conn.execute(
                "SELECT balance FROM accounts WHERE name = ?",
                (to_acc,)
            )
            to_row = cur.fetchone()
            if not to_row:
                raise AccountNotFoundError("New account not found")

            if from_row["balance"] < amount:
                raise NotEnoughMoneyError()

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