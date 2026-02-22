import pytest
from money_flow.services import AccountService
from money_flow.exceptions import NotEnoughMoneyError, AccountAlreadyExistsError, AccountNotFoundError


def test_create_account(test_db):
    service = AccountService()
    service.create_account("Cash", 100)

    accounts = service.show_accounts()
    assert len(accounts) == 1
    assert accounts[0].name == "Cash"
    assert accounts[0].balance == 100

def test_create_duplicate_account(test_db):
    service = AccountService()
    service.create_account("Cash", 100)

    with pytest.raises(AccountAlreadyExistsError):
        service.create_account("Cash", 200)

def test_topup_success(test_db):
    service = AccountService()
    service.create_account("A", 100)

    service.top_up_balance("A", 100)

    accounts = service.show_accounts()
    assert accounts[0].balance == 200

def test_transfer_success(test_db):
    service = AccountService()
    service.create_account("A", 100)
    service.create_account("B", 0)

    service.transfer("A", "B", 50)

    balances = {acc.name: acc.balance for acc in service.show_accounts()}
    assert balances["A"] == 50
    assert balances["B"] == 50

def test_transfer_not_enough_money(test_db):
    service = AccountService()
    service.create_account("A", 10)
    service.create_account("B", 0)

    with pytest.raises(NotEnoughMoneyError):
        service.transfer("A", "B", 50)

    balances = {acc.name: acc.balance for acc in service.show_accounts()}
    assert balances["A"] == 10
    assert balances["B"] == 0

def test_transfer_account_not_found(test_db):
    service = AccountService()
    service.create_account("A", 100)

    with pytest.raises(AccountNotFoundError):
        service.transfer("A", "B", 50)