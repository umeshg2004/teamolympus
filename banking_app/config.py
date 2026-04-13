from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = "sqlite:///./banking_app.db"

SECRET_KEY = "change-this-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

ADMIN_SECRET_CODE = "SSSS0987"
ADMIN_SEED_ADMINS = [
    {"username": "admin_branch_1", "password": "Adm!n-7Q2p", "full_name": "Branch Admin One", "email": "admin1@branch.local"},
    {"username": "admin_branch_2", "password": "Adm!n-9K5x", "full_name": "Branch Admin Two", "email": "admin2@branch.local"},
]
