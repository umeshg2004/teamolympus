import hashlib
import hmac

from ..config import SECRET_KEY

def hash_password(password: str) -> str:
    salted = f"{password}{SECRET_KEY}".encode("utf-8")
    return hashlib.sha256(salted).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    return hmac.compare_digest(hash_password(password), password_hash)
