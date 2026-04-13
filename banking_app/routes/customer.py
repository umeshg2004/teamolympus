from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.account import Account
from ..models.customer import Customer
from ..models.service_request import ServiceRequest
from ..schemas.transaction_schema import (
    AccountCreate,
    AccountOut,
    DepositRequest,
    WithdrawRequest,
    TransferRequest,
    CloseAccountRequest,
)
from ..schemas.customer_schema import ServiceRequestCreate
from ..services.auth_service import require_role
from ..services.transaction_service import deposit, withdraw, transfer, close_account

router = APIRouter(prefix="/customer", tags=["customer"])


def get_customer_record(db: Session, user_id: int) -> Customer:
    customer = db.query(Customer).filter(Customer.user_id == user_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer profile not found")
    return customer


@router.post("/accounts", response_model=AccountOut)
def create_account(
    payload: AccountCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("customer")),
):
    customer = get_customer_record(db, user.id)
    account = Account(customer_id=customer.id, balance=max(payload.initial_deposit, 0.0))
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.get("/accounts", response_model=list[AccountOut])
def list_accounts(
    db: Session = Depends(get_db),
    user=Depends(require_role("customer")),
):
    customer = get_customer_record(db, user.id)
    return db.query(Account).filter(Account.customer_id == customer.id).all()


@router.post("/deposit", response_model=AccountOut)
def deposit_money(
    payload: DepositRequest,
    db: Session = Depends(get_db),
    user=Depends(require_role("customer")),
):
    customer = get_customer_record(db, user.id)
    account = db.query(Account).filter(Account.id == payload.account_id, Account.customer_id == customer.id).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return deposit(db, account, payload.amount)


@router.post("/withdraw", response_model=AccountOut)
def withdraw_money(
    payload: WithdrawRequest,
    db: Session = Depends(get_db),
    user=Depends(require_role("customer")),
):
    customer = get_customer_record(db, user.id)
    account = db.query(Account).filter(Account.id == payload.account_id, Account.customer_id == customer.id).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return withdraw(db, account, payload.amount)


@router.post("/transfer")
def transfer_money(
    payload: TransferRequest,
    db: Session = Depends(get_db),
    user=Depends(require_role("customer")),
):
    customer = get_customer_record(db, user.id)
    from_account = db.query(Account).filter(
        Account.id == payload.from_account_id,
        Account.customer_id == customer.id,
    ).first()
    if not from_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source account not found")

    to_account = db.query(Account).filter(Account.id == payload.to_account_id).first()
    if not to_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target account not found")

    transfer(db, from_account, to_account, payload.amount)
    return {"status": "ok"}


@router.post("/close", response_model=AccountOut)
def close_account_endpoint(
    payload: CloseAccountRequest,
    db: Session = Depends(get_db),
    user=Depends(require_role("customer")),
):
    customer = get_customer_record(db, user.id)
    account = db.query(Account).filter(Account.id == payload.account_id, Account.customer_id == customer.id).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return close_account(db, account)


@router.post("/request")
def create_service_request(
    payload: ServiceRequestCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("customer")),
):
    customer = get_customer_record(db, user.id)
    req = ServiceRequest(customer_id=customer.id, message=payload.message)
    db.add(req)
    db.commit()
    db.refresh(req)
    return {"status": "ok", "request_id": req.id}