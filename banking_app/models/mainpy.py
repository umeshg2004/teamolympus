from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import ADMIN_SEED_ADMINS
from .database import Base, engine, SessionLocal
from .models import user, customer as customer_model, staff as staff_model, account, transaction, service_request
from .models.user import User
from .models.staff import Staff
from .routes import auth, customer, admin, staff
from .utils.hash import hash_password

Base.metadata.create_all(bind=engine)


def seed_admins() -> None:
    db = SessionLocal()
    try:
        for admin_data in ADMIN_SEED_ADMINS:
            existing = db.query(User).filter(User.username == admin_data["username"]).first()
            if existing:
                continue
            user_obj = User(
                username=admin_data["username"],
                password_hash=hash_password(admin_data["password"]),
                role="admin",
            )
            db.add(user_obj)
            db.flush()
            staff_obj = Staff(
                user_id=user_obj.id,
                full_name=admin_data["full_name"],
                email=admin_data["email"],
            )
            db.add(staff_obj)
        db.commit()
    finally:
        db.close()


seed_admins()

app = FastAPI(title="Banking App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(admin.router)
app.include_router(staff.router)


@app.get("/")
def root():
    return {"status": "ok"}