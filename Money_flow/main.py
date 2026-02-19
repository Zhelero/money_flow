from services import ExpenseService, AccountService

service = ExpenseService()
account_service = AccountService()

def main():
    print("Welcome to Money Flow!")

    while True:
        print("\ncreate, balance, topup, transfer, spend, list, delete, edit, category, total, exit")
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
            account_service.top_up_balance(destination, amount)

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

        elif task == "list":
            expenses = service.load_expenses()
            for expense in expenses:
                print(
                    f'{expense.deal_id}|{expense.amount} {expense.category} {expense.money_source}|{expense.created_at}')

        elif task == "delete":
            service.delete(int(input("What is the deal's id? ")))

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
                print(f"{e.deal_id} | {e.amount} | {e.created_at}")

        elif task == "total":
            category = input("Category (enter for all): ").strip()
            category = category if category else None
            total = service.total(category)
            print(f"Total: {total}")

        elif task == "exit":
            break

if __name__ == '__main__':
    main()