from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import Optional

from ..database import get_db
from ..models.account import Account
from ..models.customer import Customer
from ..schemas.transaction_schema import AdminAccountOut
from ..services.auth_service import require_role

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/accounts", response_model=list[AdminAccountOut])
def list_accounts(
    status: Optional[str] = Query(default=None, description="active or closed"),
    customer_id: Optional[int] = None,
    balance_min: Optional[float] = None,
    balance_max: Optional[float] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    query = db.query(Account, Customer).join(Customer, Customer.id == Account.customer_id)

    if status == "active":
        query = query.filter(Account.is_active.is_(True))
    elif status == "closed":
        query = query.filter(Account.is_active.is_(False))

    if customer_id is not None:
        query = query.filter(Account.customer_id == customer_id)

    if balance_min is not None:
        query = query.filter(Account.balance >= balance_min)

    if balance_max is not None:
        query = query.filter(Account.balance <= balance_max)

    sort_map = {
        "created_at": Account.created_at,
        "balance": Account.balance,
        "id": Account.id,
    }
    sort_col = sort_map.get(sort_by, Account.created_at)
    order_fn = desc if sort_order == "desc" else asc

    rows = query.order_by(order_fn(sort_col)).all()
    results: list[AdminAccountOut] = []
    for account, customer in rows:
        results.append(
            AdminAccountOut(
                id=account.id,
                customer_id=account.customer_id,
                customer_name=customer.full_name,
                customer_email=customer.email,
                balance=account.balance,
                is_active=account.is_active,
                created_at=account.created_at,
            )
        )
    return results
