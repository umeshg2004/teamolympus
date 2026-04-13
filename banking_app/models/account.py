from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base


# ----------------------------------------------------
# Account Model
# Represents a bank account belonging to a customer
# ----------------------------------------------------

class Account(Base):
    __tablename__ = "accounts"

    # primary key of the account table
    id = Column(Integer, primary_key=True, index=True)

    # reference to the customer who owns this account
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    # current account balance
    balance = Column(Float, default=0.0, nullable=False)

    # account status (active / closed)
    is_active = Column(Boolean, default=True, nullable=False)

    # account creation timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relationship with Customer model
    customer = relationship("Customer", back_populates="accounts")

    # relationship with Transaction model
    transactions = relationship("Transaction", back_populates="account")
