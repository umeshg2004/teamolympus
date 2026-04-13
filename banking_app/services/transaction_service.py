from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.account import Account
from ..models.transaction import Transaction


def deposit(db: Session, account: Account, amount: float) -> Account:
    if amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be positive")
    if not account.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account is closed")
    account.balance += amount
    db.add(Transaction(account_id=account.id, type="deposit", amount=amount))
    db.commit()
    db.refresh(account)
    return account


def withdraw(db: Session, account: Account, amount: float) -> Account:
    if amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be positive")
    if not account.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account is closed")
    if account.balance < amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")
    account.balance -= amount
    db.add(Transaction(account_id=account.id, type="withdraw", amount=amount))
    db.commit()
    db.refresh(account)
    return account


def transfer(db: Session, from_account: Account, to_account: Account, amount: float) -> None:
    if amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be positive")
    if not from_account.is_active or not to_account.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account is closed")
    if from_account.balance < amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")

    from_account.balance -= amount
    to_account.balance += amount

    db.add(Transaction(account_id=from_account.id, type="transfer_out", amount=amount, target_account_id=to_account.id))
    db.add(Transaction(account_id=to_account.id, type="transfer_in", amount=amount, target_account_id=from_account.id))
    db.commit()


def close_account(db: Session, account: Account) -> Account:
    if not account.is_active:
        return account
    if account.balance != 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Balance must be zero to close")
    account.is_active = False
    db.commit()
    db.refresh(account)
    return account