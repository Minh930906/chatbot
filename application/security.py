from datetime import datetime, timedelta
from typing import Optional
from dotenv import dotenv_values

from jose import jwt
from passlib.context import CryptContext

secrets = dotenv_values(".env")

SECRET_KEY = secrets["SECRET_KEY"]
ALGORITHM = secrets["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = secrets["ACCESS_TOKEN_EXPIRE_MINUTES"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt
