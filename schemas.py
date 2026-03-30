from pydantic import BaseModel, Field
from datetime import datetime

class AccountCreate(BaseModel):
    name: str = Field(..., min_length=1)
    balance: float = Field(..., ge=0)

class AccountResponse(BaseModel):
    name: str
    balance: float

class TransferRequest(BaseModel):
    from_account: str = Field(..., min_length=1)
    to_account: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)

class TopUpRequest(BaseModel):
    amount: float = Field(..., gt=0)

class ExpenseCreate(BaseModel):
    amount: float = Field(..., gt=0)
    money_source: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)

class ExpenseResponse(BaseModel):
    deal_id: int
    amount: float
    money_source: str
    category: str
    created_at: datetime

class ExpenseUpdate(BaseModel):
    amount: float | None = Field(default=None, gt=0)
    money_source: str | None = Field(default=None, min_length=1)
    category: str | None = Field(default=None, min_length=1)

class TotalResponse(BaseModel):
    total: float