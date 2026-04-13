from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base


# ----------------------------------------------------
# User Model
# Stores login credentials and role of the system user
# Roles: customer, staff, admin
# ----------------------------------------------------

class User(Base):
    __tablename__ = "users"

    # unique user id
    id = Column(Integer, primary_key=True, index=True)

    # username used for authentication
    username = Column(String, unique=True, index=True, nullable=False)

    # hashed password stored securely
    password_hash = Column(String, nullable=False)

    # role of the user (customer / staff / admin)
    role = Column(String, nullable=False)

    # timestamp when the user was created
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relationship with Customer profile
    customer = relationship("Customer", back_populates="user", uselist=False)

    # relationship with Staff profile
    staff = relationship("Staff", back_populates="user", uselist=False)
