from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class RegisterRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: str  # customer, staff, admin
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    secret_code: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    role: str  # customer, admin, staff
    secret_code: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CustomerOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class ServiceRequestCreate(BaseModel):
    message: str


class ServiceRequestOut(BaseModel):
    id: int
    message: str
    status: str
    created_at: datetime
    customer_id: int
    customer_name: str
    customer_email: EmailStr
    customer_phone: Optional[str] = None

    class Config:
        orm_mode = True


class ServiceRequestUpdate(BaseModel):
    status: str  # open or solved
