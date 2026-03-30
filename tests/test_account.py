import pytest
from exceptions import NotEnoughMoneyError, AccountAlreadyExistsError, AccountNotFoundError


def test_create_account(acc_service):
    acc_service.create_account("Cash", 100)

    accounts = acc_service.show_accounts()
    assert len(accounts) == 1
    assert accounts[0].name == "Cash"
    assert accounts[0].balance == 100

def test_create_duplicate_account(acc_service):
    acc_service.create_account("Cash", 100)

    with pytest.raises(AccountAlreadyExistsError):
        acc_service.create_account("Cash", 200)

def test_top_up_success(acc_service):
    acc_service.create_account("A", 100)

    acc_service.top_up_balance("A", 100)

    accounts = acc_service.show_accounts()
    assert accounts[0].balance == 200

def test_transfer_success(acc_service):
    acc_service.create_account("A", 100)
    acc_service.create_account("B", 0)

    acc_service.transfer("A", "B", 50)

    balances = {acc.name: acc.balance for acc in acc_service.show_accounts()}
    assert balances["A"] == 50
    assert balances["B"] == 50

def test_transfer_not_enough_money(acc_service):
    acc_service.create_account("A", 10)
    acc_service.create_account("B", 0)

    with pytest.raises(NotEnoughMoneyError):
        acc_service.transfer("A", "B", 50)

    balances = {acc.name: acc.balance for acc in acc_service.show_accounts()}
    assert balances["A"] == 10
    assert balances["B"] == 0

def test_transfer_account_not_found(acc_service):
    acc_service.create_account("A", 100)

    with pytest.raises(AccountNotFoundError):
        acc_service.transfer("A", "B", 50)