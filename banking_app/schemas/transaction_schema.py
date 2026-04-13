from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AccountCreate(BaseModel):
    initial_deposit: float = 0.0


class AccountOut(BaseModel):
    id: int
    customer_id: int
    balance: float
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class AdminAccountOut(BaseModel):
    id: int
    customer_id: int
    customer_name: str
    customer_email: str
    balance: float
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class TransactionOut(BaseModel):
    id: int
    account_id: int
    type: str
    amount: float
    target_account_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True


class DepositRequest(BaseModel):
    account_id: int
    amount: float


class WithdrawRequest(BaseModel):
    account_id: int
    amount: float


class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float


class CloseAccountRequest(BaseModel):
    account_id: int
