from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status

from exceptions import (
    AccountNotFoundError,
    ExpenseNotFoundError,
    NotEnoughMoneyError,
    InvalidAmountError,
)

def register_exception_handlers(app):

    @app.exception_handler(AccountNotFoundError)
    async def account_not_found_handler(request: Request, exc: AccountNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc) or "Account not found"},
        )

    @app.exception_handler(ExpenseNotFoundError)
    async def expense_not_found_handler(request: Request, exc: ExpenseNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc) or "Expense not found"},
        )

    @app.exception_handler(NotEnoughMoneyError)
    async def not_enough_money_handler(request: Request, exc: NotEnoughMoneyError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc) or "Not enough money"},
        )

    @app.exception_handler(InvalidAmountError)
    async def invalid_amount_handler(request: Request, exc: InvalidAmountError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc) or "Invalid amount"},
        )