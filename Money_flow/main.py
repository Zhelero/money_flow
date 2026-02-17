from service import ExpenseService

service = ExpenseService()

def main():
    print("Welcome to Money Flow!")

    while True:
        print("\nadd, list, delete, edit, category, total, exit")
        task = input("What would you like to do? ").strip()

        if task == "add":
            amount = float(input("What is the amount you've spent? "))
            source = input("where does the money come from? ")
            category = input("What is the category? ")
            service.spend(amount, source, category)

        elif task == "list":
            expenses = service.load_expenses()
            for expense in expenses:
                print(f'{expense.deal_id}|{expense.amount} {expense.category} {expense.money_source}|{expense.created_at}')

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







