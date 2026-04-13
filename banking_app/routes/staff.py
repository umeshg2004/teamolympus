from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.service_request import ServiceRequest
from ..models.customer import Customer
from ..schemas.customer_schema import ServiceRequestOut
from ..services.auth_service import require_role

router = APIRouter(prefix="/staff", tags=["staff"])


@router.get("/requests", response_model=list[ServiceRequestOut])
def list_requests(
    db: Session = Depends(get_db),
    user=Depends(require_role("staff", "admin")),
):
    rows = (
        db.query(ServiceRequest, Customer)
        .join(Customer, Customer.id == ServiceRequest.customer_id)
        .order_by(ServiceRequest.created_at.desc())
        .all()
    )

    results: list[ServiceRequestOut] = []
    for req, customer in rows:
        results.append(
            ServiceRequestOut(
                id=req.id,
                message=req.message,
                status=req.status,
                created_at=req.created_at,
                customer_id=customer.id,
                customer_name=customer.full_name,
                customer_email=customer.email,
            )
        )
    return results