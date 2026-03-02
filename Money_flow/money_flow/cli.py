#Money Flow 1.0 CLI
from .services import ExpenseService, AccountService
from .repositories import ExpenseRepository, AccountRepository
from .exceptions import MoneyFlowError
from .database import db_instance
from .config import config
import logging

#---Bootstrap---
def bootstrap():
    expense_repo = ExpenseRepository(db_instance)
    account_repo = AccountRepository(db_instance)

    expense_service = ExpenseService(expense_repo, account_repo)
    account_service = AccountService(account_repo)

    return expense_service, account_service

#CLI

#Create app logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

#Log format
formatter = logging.Formatter("%(asctime)s || %(name)s || %(levelname)s || %(message)s")

#-----APP LOG(INFO и выше)-----
app_handler = logging.FileHandler("app.log")
app_handler.setLevel(logging.INFO)
app_handler.setFormatter(formatter)

#-----ERROR LOG-----
error_handler = logging.FileHandler("error.log")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

#Add handlers to logger
if not root_logger.handlers:
    root_logger.addHandler(app_handler)
    root_logger.addHandler(error_handler)

def main():
    service, account_service = bootstrap()

    print("Welcome to Money Flow!")

    while True:
        print("\ncreate, balance, topup, transfer, spend, list, delete, edit, category, total, exit")
        try:
            task = input("What would you like to do? ").strip()

            if task == "create":
                source = input("How to name payment method? ").strip()
                initial_balance = float(input("What is the initial balance? ").strip())
                account_service.create_account(source, initial_balance)

            elif task == "balance":
                accounts = account_service.show_accounts()
                if not accounts:
                    print("No accounts yet")
                else:
                    for acc in accounts:
                        print(f"{acc.name}: {acc.balance}")

            elif task == "topup":
                destination = input("Top up what? ")
                amount = float(input("How much to add? "))
                new_balance = account_service.top_up_balance(destination, amount)
                print(f"New balance: {new_balance}")

            elif task == "transfer":
                source = input("What would you like to transfer from? ").strip()
                destination = input("What would you like to transfer to? ").strip()
                amount = float(input("How much to transfer? "))
                account_service.transfer(source, destination, amount)

            elif task == "spend":
                amount = float(input("What is the amount you've spent? "))
                source = input("where does the money come from? ")
                category = input("What is the category? ")
                service.spend(amount, source, category)
                print("Money spent")

            elif task == "list":
                expenses = service.load_expenses()
                if not expenses:
                    print("No expenses yet")
                else:
                    for expense in expenses:
                        print(
                            f'{expense.deal_id} || {expense.amount} - {expense.category} - {expense.money_source} | {expense.created_at}')

            elif task == "delete":
                service.delete(int(input("What is the deal's id? ")))
                print("Expense deleted")

            elif task == "edit":
                deal_id = int(input("Deal id: "))
                amount_input = input("New amount (enter to skip): ")
                source_input = input("New source (enter to skip): ")
                category_input = input("New category (enter to skip): ")

                amount = float(amount_input) if amount_input else None
                source = source_input if source_input else None
                category = category_input if category_input else None

                service.edit(deal_id, amount, source, category)

            elif task == "category":
                category = input("Which category to show? ")
                expenses = service.by_category(category)

                for e in expenses:
                    print(f"{e.deal_id} || {e.amount} - {e.created_at}")

            elif task == "total":
                category = input("Category (enter for all): ").strip()
                category = category if category else None
                total = service.total(category)
                print(f"Total: {total}")

            elif task == "exit":
                break

            elif task == "__reset__":
                if not config.DEBUG:
                    print("Command not available")
                    continue

                confirm = input("Are you sure? Type YES to confirm: ")
                if confirm == "YES":
                    db_instance.reset()
                    logger.warning("Database reset performed")
                    print("Database cleared")

            else:
                print("Unknown command")

        except ValueError:
            print("Invalid number format")

        except MoneyFlowError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()