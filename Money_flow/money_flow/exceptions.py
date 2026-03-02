class MoneyFlowError(Exception):
    status_code = 400
    default_message = "Money Flow Error"

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)

class AccountNotFoundError(MoneyFlowError):
    status_code = 404
    default_message = "Account Not Found"

class NotEnoughMoneyError(MoneyFlowError):
    status_code = 400
    default_message = "Not Enough Money"

class AccountAlreadyExistsError(MoneyFlowError):
    status_code = 400
    default_message = "Account Already Exists"

class ExpenseNotFoundError(MoneyFlowError):
    status_code = 404
    default_message = "Expense Not Found"

class InvalidAmountError(MoneyFlowError):
    status_code = 400
    default_message = "Amount must be greater than zero"