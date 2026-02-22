class MoneyFlowError(Exception):
    pass

class AccountNotFoundError(MoneyFlowError):
    pass

class NotEnoughMoneyError(MoneyFlowError):
    pass

class AccountAlreadyExistsError(MoneyFlowError):
    pass

class DealNotFoundError(MoneyFlowError):
    pass

class ExpenseNotFoundError(MoneyFlowError):
    pass