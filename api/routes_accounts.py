from fastapi import APIRouter, Depends, status
from typing import List

from services import AccountService
from schemas import AccountCreate, AccountResponse, TransferRequest, TopUpRequest
from dependencies import get_account_service

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    data: AccountCreate,
    service: AccountService = Depends(get_account_service),
):
    account = service.create_account(data.name, data.balance)
    return account

@router.get("/", response_model=List[AccountResponse])
def read_accounts(
    service: AccountService = Depends(get_account_service),
):
    return service.show_accounts()

@router.post("/{account_name}/topup", response_model=AccountResponse)
def topup_balance(
        account_name: str,
        data: TopUpRequest,
        service: AccountService = Depends(get_account_service),
):
    new_balance = service.topup_balance(account_name, data.amount)

    return AccountResponse(
        name=account_name,
        balance=new_balance,)

@router.post("/transfer", status_code=status.HTTP_204_NO_CONTENT)
def transfer_money(
    data: TransferRequest,
    service: AccountService = Depends(get_account_service),
):
    service.transfer(
        from_acc=data.from_account,
        to_acc=data.to_account,
        amount=data.amount,
    )