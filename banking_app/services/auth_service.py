from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models.user import User
from ..models.customer import Customer
from ..models.staff import Staff
from ..utils.hash import hash_password, verify_password
from ..utils.jwt import create_access_token, try_decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_user(db: Session, username: str, password: str, role: str) -> User:
    user = User(username=username, password_hash=hash_password(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str, role: str) -> Optional[User]:
    user: Optional[User] = None
    if role == "customer":
        customer = db.query(Customer).filter(Customer.email == email).first()
        if customer:
            user = db.query(User).filter(User.id == customer.user_id, User.role == "customer").first()
    elif role in {"admin", "staff"}:
        staff = db.query(Staff).filter(Staff.email == email).first()
        if staff:
            user = db.query(User).filter(User.id == staff.user_id, User.role == role).first()

    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = try_decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_role(*roles: str):
    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        return user

    return checker


def build_token(user: User) -> str:
    return create_access_token({"sub": str(user.id), "role": user.role})
