from repositories import ExpenseRepository, AccountRepository
from models import Expense, Account

class ExpenseService:
    def __init__(self):
        self.repo = ExpenseRepository()
        self.account_repo = AccountRepository()

    def spend(self, amount, money_source, category):
        expense = Expense.create(amount, money_source, category)
        self.repo.spend(expense)
        self.account_repo.update_balance(money_source, -amount)
        print("Money spent")

    def load_expenses(self):
        return self.repo.load()

    def delete(self, deal_id):
        self.repo.delete(deal_id)
        print('Expense deleted')

    def edit(self, deal_id, amount=None, money_source=None, category=None):
        expenses = self.repo.load()
        for expense in expenses:
            if deal_id == expense.deal_id:
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

                print(f"Edited expense #{deal_id}")
                return

        print("Expense not found")

    def by_category(self, category):
        return [e for e in self.repo.load() if e.category == category]

    def total(self, category=None):
        return self.repo.total(category)


class AccountService:
    def __init__(self):
        self.repo = AccountRepository()

    def create_account(self, name, balance):
        account = Account.create(name, balance)
        self.repo.create_account(account)

    def show_accounts(self):
        return self.repo.get_accounts()

    def transfer(self, from_acc, to_acc, amount):
        self.repo.update_balance(from_acc, -amount)
        try:
            self.repo.update_balance(to_acc, amount)
        except:
            self.repo.update_balance(from_acc, amount)
            raise

    def top_up_balance(self, name, amount):
        return self.repo.update_balance(name, amount)