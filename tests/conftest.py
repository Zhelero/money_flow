import pytest
from database import Database
from config import config
from repositories import AccountRepository, ExpenseRepository
from services import AccountService, ExpenseService


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    test_db_path = tmp_path / "test.db"
    monkeypatch.setattr(config, "DB_NAME", str(test_db_path))

    Database()
    yield

@pytest.fixture
def acc_service(test_db):
    db = Database()
    return AccountService(AccountRepository(db))

@pytest.fixture
def exp_service(test_db):
    db = Database()
    return ExpenseService(ExpenseRepository(db), AccountRepository(db))