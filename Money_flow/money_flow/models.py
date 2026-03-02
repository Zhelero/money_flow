from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Expense:
    deal_id: int | None
    amount: float
    money_source: str
    category: str
    created_at: str

    @staticmethod
    def create(amount: float, money_source: str, category: str):
        if amount < 0:
            raise ValueError("Amount must be positive")

        return Expense(
            deal_id=None,
            amount=amount,
            money_source=money_source,
            category=category,
            created_at=datetime.now().isoformat()
        )

@dataclass(frozen=True)
class Account:
    account_id: int | None
    name: str
    balance: float

    @staticmethod
    def create(name: str, balance: float):
        return Account(
            account_id=None,
            name=name,
            balance=balance
        )