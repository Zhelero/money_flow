from dataclasses import dataclass
from datetime import datetime


@dataclass
class Expense:
    deal_id: int | None
    amount: float
    money_source: str
    category: str
    created_at: str

    @staticmethod
    def create(amount, money_source, category):
        return Expense(
            deal_id=None,
            amount=amount,
            money_source=money_source,
            category=category,
            created_at=datetime.now().isoformat(timespec="minutes")
        )

@dataclass
class Account:
    account_id: int | None
    name: str
    balance: float

    @staticmethod
    def create(name, balance):
        return Account(
            account_id=None,
            name=name,
            balance=balance
        )