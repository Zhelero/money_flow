from fastapi import Depends
from database import db_instance, Database
from repositories import ExpenseRepository, AccountRepository
from services import ExpenseService, AccountService

def get_database() -> Database:
    return db_instance

def get_expense_repo(db: Database = Depends(get_database)):
    return ExpenseRepository(db)

def get_account_repo(db: Database = Depends(get_database)):
    return AccountRepository(db)

def get_expense_service(
    expense_repo: ExpenseRepository = Depends(get_expense_repo),
    account_repo: AccountRepository = Depends(get_account_repo),
):
    return ExpenseService(expense_repo, account_repo)

def get_account_service(
        account_repo: AccountRepository = Depends(get_account_repo),
) -> AccountService:
    return AccountService(account_repo)