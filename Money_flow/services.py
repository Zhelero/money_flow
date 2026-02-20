from exceptions import AccountNotFoundError, DealNotFoundError
from repositories import ExpenseRepository, AccountRepository
from models import Expense, Account
#from exceptions import MoneyFlowError
import logging

logger = logging.getLogger(__name__)

class ExpenseService:
    def __init__(self):
        self.repo = ExpenseRepository()
        self.account_repo = AccountRepository()

    def spend(self, amount, money_source, category):
        logger.info(f"Attempting to spend {amount} from {money_source} at {category}")
        expense = Expense.create(amount, money_source, category)
        self.repo.spend_atomic(expense)
        print("Money spent")
        logger.info(f"Money spent successfully")

    def load_expenses(self):
        return self.repo.load()

    def delete(self, deal_id):
            self.repo.delete(deal_id)

    def edit(self, deal_id, amount=None, money_source=None, category=None):
        expense = self.repo.get_by_id(deal_id)

        old_amount = expense.amount
        old_source = expense.money_source

        if amount is not None:
            expense.amount = amount

        if money_source is not None:
            expense.money_source = money_source

        if category is not None:
            expense.category = category

        self.repo.update(expense)

        if old_source == expense.money_source:
            delta = old_amount - expense.amount
            self.account_repo.update_balance(expense.money_source, delta)
        else:
            self.account_repo.update_balance(old_source, old_amount)
            self.account_repo.update_balance(expense.money_source, -expense.amount)

    def by_category(self, category):
        return [e for e in self.repo.load() if e.category == category]

    def total(self, category=None):
        return self.repo.total(category)


class AccountService:
    def __init__(self):
        self.repo = AccountRepository()

    def create_account(self, name, balance):
        logger.info(f"Attempting to create account {name} with balance {balance}")
        account = Account.create(name, balance)
        self.repo.create_account(account)

    def show_accounts(self):
        return self.repo.get_accounts()

    def transfer(self, from_acc, to_acc, amount):
        logger.info(f"Transfer {amount} from {from_acc} to {to_acc}")
        self.repo.update_balance(from_acc, -amount)
        try:
            self.repo.update_balance(to_acc, amount)
            logger.info("Transfer completed")
        except Exception:
            logger.error("Transfer failed, rolling back", exc_info=True)
            self.repo.update_balance(from_acc, amount)
            raise

    def top_up_balance(self, name, amount):
        return self.repo.update_balance(name, amount)