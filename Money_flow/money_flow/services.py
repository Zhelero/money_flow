from .repositories import ExpenseRepository, AccountRepository
from .models import Expense, Account
from .exceptions import InvalidAmountError
import logging

logger = logging.getLogger(__name__)

class ExpenseService:
    def __init__(self, expense_repo: ExpenseRepository, account_repo: AccountRepository):
        self.repo = expense_repo
        self.account_repo = account_repo

    def spend(self, amount: float, money_source: str, category: str | None):
        if amount <= 0:
            logger.error("Expense amount cannot be negative")
            raise InvalidAmountError()

        logger.info(f"Attempting to spend {amount} from {money_source} at {category}")
        expense = Expense.create(amount, money_source, category)
        self.repo.spend_atomic(expense)
        logger.info(f"Money spent successfully")
        return expense

    def load_expenses(self):
        return self.repo.load()

    def delete(self, deal_id):
        self.repo.delete(deal_id)

    def edit(self, deal_id, amount=None, money_source=None, category=None):
        if amount is not None and amount <= 0:
            logger.error(f"Invalid amount {amount}")
            raise InvalidAmountError()

        self.repo.edit_atomic(deal_id, amount, money_source, category)

    def by_category(self, category):
        return self.repo.by_category(category)

    def total(self, category=None):
        return self.repo.total(category)


class AccountService:
    def __init__(self, account_repo: AccountRepository):
        self.repo = account_repo

    def create_account(self, name: str, balance: float) -> Account:
        if balance < 0:
            logger.error("Account balance cannot be negative")
            raise InvalidAmountError()

        logger.info(f"Attempting to create account {name} with balance {balance}")
        account = Account.create(name, balance)
        self.repo.create_account(account)
        return account

    def show_accounts(self):
        return self.repo.get_accounts()

    def transfer(self, from_acc: str, to_acc: str, amount: float):
        if amount <= 0:
            logger.error(f"Invalid amount {amount}")
            raise InvalidAmountError()

        logger.info(f"Transfer {amount} from {from_acc} to {to_acc}")
        self.repo.transfer_atomic(from_acc, to_acc, amount)
        logger.info("Transfer completed")

    def top_up_balance(self, name: str, amount: float):
        if amount <= 0:
            logger.error(f"Invalid amount {amount}")
            raise InvalidAmountError()

        return self.repo.update_balance(name, amount)
