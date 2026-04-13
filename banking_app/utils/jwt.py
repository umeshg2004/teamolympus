from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import JWTError, jwt

from ..config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def try_decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        return decode_token(token)
    except JWTError:
        return None