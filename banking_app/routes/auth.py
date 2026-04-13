from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..config import ADMIN_SECRET_CODE
from ..database import get_db
from ..models.user import User
from ..models.customer import Customer
from ..models.account import Account
from ..models.staff import Staff
from ..schemas.customer_schema import RegisterRequest, LoginRequest, TokenResponse
from ..services.auth_service import authenticate_user, build_token, create_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if payload.role not in {"customer", "staff", "admin"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")

    if payload.role == "admin":
        if not payload.secret_code or payload.secret_code != ADMIN_SECRET_CODE:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid admin secret code")

    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    user = create_user(db, payload.username, payload.password, payload.role)

    if payload.role == "customer":
        customer = Customer(
            user_id=user.id,
            full_name=payload.full_name,
            email=payload.email,
            phone=payload.phone,
        )
        db.add(customer)
        db.flush()
        account = Account(customer_id=customer.id, balance=0.0)
        db.add(account)
    else:
        staff = Staff(
            user_id=user.id,
            full_name=payload.full_name,
            email=payload.email,
        )
        db.add(staff)

    db.commit()
    token = build_token(user)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    if payload.role not in {"customer", "admin", "staff"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
    user = authenticate_user(db, payload.email, payload.password, payload.role)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = build_token(user)
    return TokenResponse(access_token=token)
