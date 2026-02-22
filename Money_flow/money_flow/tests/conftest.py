import pytest
from money_flow.database import Database
from money_flow.config import config

@pytest.fixture
def test_db(tmp_path, monkeypatch):
    test_db_path = tmp_path / "test.db"
    monkeypatch.setattr(config, "DB_NAME", str(test_db_path))

    db =Database()
    yield

@pytest.fixture
def services(test_db):
    from money_flow.services import AccountService, ExpenseService
    return AccountService(), ExpenseService()