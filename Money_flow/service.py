from repository import ExpenseRepository
from models import Expense

class ExpenseService:
    def __init__(self):
        self.repo = ExpenseRepository()

    def spend(self, amount, money_source, category):
        expense = Expense.create(amount, money_source, category)
        self.repo.spend(expense)
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
                if amount is not None:
                    expense.amount = amount

                if money_source is not None:
                    expense.money_source = money_source

                if category is not None:
                    expense.category = category

                self.repo.update(expense)
                print(f"Edited expense #{deal_id}")
                return

        print("Expense not found")

    def by_category(self, category):
        return [e for e in self.repo.load() if e.category == category]

    def total(self, category=None):
        return self.repo.total(category)

