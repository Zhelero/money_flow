import pytest
from money_flow.services import ExpenseService, AccountService
from money_flow.exceptions import NotEnoughMoneyError, AccountNotFoundError, ExpenseNotFoundError


def test_spend_success(test_db):
    acc_service = AccountService()
    exp_service = ExpenseService()

    acc_service.create_account("Cash", 100)

    exp_service.spend(50, "Cash", "Food")

    accounts = acc_service.show_accounts()
    assert accounts[0].balance == 50

    expenses = exp_service.load_expenses()
    assert len(expenses) == 1
    assert expenses[0].amount == 50

def test_spend_not_enough_money(test_db):
    acc_service = AccountService()
    exp_service = ExpenseService()

    acc_service.create_account("Cash", 10)

    with pytest.raises(NotEnoughMoneyError):
        exp_service.spend(50, "Cash", "Food")

    accounts = acc_service.show_accounts()
    assert accounts[0].balance == 10

def test_spend_account_not_found(test_db):
    exp_service = ExpenseService()

    with pytest.raises(AccountNotFoundError):
        exp_service.spend(50, "Cash", "Food")

def test_edit_success(test_db):
    acc_service = AccountService()
    exp_service = ExpenseService()

    acc_service.create_account("Cash", 100)
    exp_service.spend(50, "Cash", "Food")

    expense = exp_service.load_expenses()[0]
    exp_service.edit(expense.deal_id, 80)

    expense = exp_service.load_expenses()[0]
    assert expense.amount == 80

    accounts = acc_service.show_accounts()
    assert accounts[0].balance == 20

def test_edit_increase_amount_not_enough_money(test_db):
    acc_service = AccountService()
    exp_service = ExpenseService()

    acc_service.create_account("Cash", 80)
    exp_service.spend(50, "Cash", "Food")

    expense = exp_service.load_expenses()[0]

    with pytest.raises(NotEnoughMoneyError):
        exp_service.edit(expense.deal_id, amount=150)

    accounts = acc_service.show_accounts()
    assert accounts[0].balance == 30

def test_edit_change_account_success(test_db):
    acc_service = AccountService()
    exp_service = ExpenseService()

    acc_service.create_account("A", 100)
    acc_service.create_account("B", 100)

    exp_service.spend(50, "A", "Food")

    expense = exp_service.load_expenses()[0]
    exp_service.edit(expense.deal_id, money_source="B")
    expense = exp_service.load_expenses()[0]

    balances = {acc.name: acc.balance for acc in acc_service.show_accounts()}

    assert balances["A"] == 100
    assert balances["B"] == 50

def test_edit_change_account_not_enough_money(test_db):
    acc_service = AccountService()
    exp_service = ExpenseService()

    acc_service.create_account("A", 100)
    acc_service.create_account("B", 10)

    exp_service.spend(50, "A", "Food")
    expense = exp_service.load_expenses()[0]

    with pytest.raises(NotEnoughMoneyError):
        exp_service.edit(expense.deal_id, money_source="B")

    balances = {acc.name: acc.balance for acc in acc_service.show_accounts()}

    assert balances["A"] == 50
    assert balances["B"] == 10

def test_edit_not_found(test_db):
    exp_service = ExpenseService()

    with pytest.raises(ExpenseNotFoundError):
        exp_service.edit(50, "A")

def test_delete_success(test_db):
    acc_service = AccountService()
    exp_service = ExpenseService()

    acc_service.create_account("Cash", 100)
    exp_service.spend(50, "Cash", "Food")

    expense = exp_service.load_expenses()[0]
    exp_service.delete(expense.deal_id)

    assert len(exp_service.load_expenses()) == 0

    accounts = acc_service.show_accounts()
    assert accounts[0].balance == 100

def test_delete_unsuccessful(test_db):
    acc_service = AccountService()
    exp_service = ExpenseService()

    acc_service.create_account("Cash", 100)
    exp_service.spend(50, "Cash", "Food")

    with pytest.raises(ExpenseNotFoundError):
        exp_service.delete(50)

def test_total(test_db):
    acc_service = AccountService()
    exp_service = ExpenseService()

    acc_service.create_account("Cash", 100)
    exp_service.spend(50, "Cash", "Food")

    assert exp_service.total() == 50

def test_total_category(test_db):
    acc_service = AccountService()
    exp_service = ExpenseService()

    acc_service.create_account("Cash", 100)
    exp_service.spend(50, "Cash", "Food")
    exp_service.spend(20, "Cash", "Health")

    assert exp_service.total("Food") == 50
